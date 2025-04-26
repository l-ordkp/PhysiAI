from pinecone import Pinecone, ServerlessSpec
import os
from typing import List, Dict, Any
from utils.embedder import LocalEmbedder
from dotenv import load_dotenv
load_dotenv(override=True)
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("INDEX_NAME")

class VectorStore:
    """
    Store and retrieve vectors using Pinecone
    """
    def __init__(self):
        """
        Initialize vector store for document chunks
        Args:
            api_key (str): Pinecone API key
            environment (str): Pinecone environment
            index_name (str): Name of Pinecone index
            embedder: Embedding provider
        """
        self.environment = pinecone_env
        self.index_name = pinecone_index_name
        self.embedder = LocalEmbedder()
        
        # Connect to Pinecone
        self.pc = Pinecone(api_key=pinecone_api_key)
        self.index = self.pc.Index(self.index_name)
    
    def store_chunks_with_questions(self, chunks_with_questions: List[Dict[str, Any]]):
        """
        Store question-only embeddings with chunk metadata in Pinecone.
        Args:
            chunks_with_questions (List[Dict]): Content chunks with generated questions
        """
        vectors = []

        for chunk_data in chunks_with_questions:
            chunk_id = chunk_data["chunk_id"]
            questions = chunk_data["questions"]

            for q_idx, question in enumerate(questions):
                embedding = self.embedder.get_embedding(question)
                vector_id = f"{chunk_id}_q{q_idx+1}"

                metadata = {
                    "chunk_id": chunk_id,
                    "content": chunk_data["content"],  # stored only as metadata
                    "content_type": chunk_data["content_type"],
                    "page": chunk_data["page"],
                    "question": question,
                    "question_idx": q_idx
                }

                if chunk_data["content_type"] == "table" and "html" in chunk_data:
                    metadata["html"] = chunk_data["html"]

                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": metadata
                })

        # Upsert in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)

        print(f"Stored {len(vectors)} question vectors in Pinecone.")

    def retrieve_content_from_query(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content chunks based on the user query.
        
        Args:
            query (str): User's natural language question.
            top_k (int): Number of top results to return.

        Returns:
            List[Dict]: Retrieved metadata chunks corresponding to relevant questions.
        """
        # Step 1: Embed the user query
        query_embedding = self.embedder.get_embedding(query)

        # Step 2: Query Pinecone for similar questions
        try:
            response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
        except Exception as e:
            print(f"Error during Pinecone query: {e}")
            return []

        # Step 3: Extract only the 'content' from metadata
        relevant_contents = [
            match.metadata.get("content", "") 
            for match in response.matches if "content" in match.metadata
        ]

        return relevant_contents
