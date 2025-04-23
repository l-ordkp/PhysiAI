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
        Store chunks with their questions in Pinecone
        Args:
            chunks_with_questions (List[Dict]): Content chunks with generated questions
        """
        vectors = []
        
        for chunk_data in chunks_with_questions:
            chunk_id = chunk_data["chunk_id"]
            questions = chunk_data["questions"]
            
            # Compute embeddings for each question
            for q_idx, question in enumerate(questions):
                # Get embedding vector for the question
                embedding = self.embedder.get_embedding(question)
                
                # Create a unique ID for this question
                vector_id = f"{chunk_id}_q{q_idx+1}"
                
                # Store the chunk as metadata
                metadata = {
                    "chunk_id": chunk_id,
                    "content": chunk_data["content"],
                    "content_type": chunk_data["content_type"],
                    "page": chunk_data["page"],
                    "question": question,
                    "question_idx": q_idx
                }
                
                # Add HTML if it's a table
                if chunk_data["content_type"] == "table" and "html" in chunk_data:
                    metadata["html"] = chunk_data["html"]
                
                vectors.append((vector_id, embedding, metadata))
                
        # Upsert vectors in batches (Pinecone has limits on batch size)
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)
            
        print(f"Stored {len(vectors)} question vectors in Pinecone.")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks based on query similarity to questions
        Args:
            query (str): Search query
            top_k (int): Number of results to return
        Returns:
            List[Dict]: Search results
        """
        # Get embedding for the query
        query_embedding = self.embedder.get_embedding(query)
        
        # Search in Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extract and format the results
        formatted_results = []
        seen_chunks = set()  # To avoid duplicate chunks
        
        for match in results["matches"]:
            chunk_id = match["metadata"]["chunk_id"]
            if chunk_id not in seen_chunks:
                seen_chunks.add(chunk_id)
                
                formatted_results.append({
                    "score": match["score"],
                    "chunk_id": chunk_id,
                    "content": match["metadata"]["content"],
                    "content_type": match["metadata"]["content_type"],
                    "page": match["metadata"]["page"],
                    "matched_question": match["metadata"]["question"],
                    "html": match["metadata"].get("html")  # Include HTML for tables if available
                })
                
        return formatted_results