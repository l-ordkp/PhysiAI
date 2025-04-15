import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorDBManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize vector database manager.
        
        Args:
            model_name (str): Model name for sentence transformer
        """
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.metadata = []
        self.questions = []
    
    def create_index(self, questions, chunks, metadata):
        """
        Create FAISS index from questions.
        
        Args:
            questions (list): List of questions
            chunks (list): List of chunks
            metadata (list): List of metadata
        """
        self.chunks = chunks
        self.metadata = metadata
        self.questions = questions
        
        # Generate embeddings
        embeddings = self.model.encode(questions)
        
        # Normalize embeddings (required for cosine similarity)
        faiss.normalize_L2(embeddings)
        
        # Create index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        self.index.add(embeddings)
    
    def save_index(self, path):
        """
        Save FAISS index to file.
        
        Args:
            path (str): Path to save the index
        """
        if self.index is not None:
            faiss.write_index(self.index, path)
    
    def load_index(self, path):
        """
        Load FAISS index from file.
        
        Args:
            path (str): Path to load the index from
        """
        self.index = faiss.read_index(path)
    
    def query(self, query_text, top_k=3):
        """
        Query the vector database.
        
        Args:
            query_text (str): Query text
            top_k (int): Number of results to return
            
        Returns:
            list: Top k results with chunks and metadata
        """
        if self.index is None:
            raise ValueError("Index not created or loaded")
        
        # Encode the query
        query_vector = self.model.encode([query_text])
        faiss.normalize_L2(query_vector)
        
        # Search the index
        distances, indices = self.index.search(query_vector, top_k)
        
        # Get the matching chunks and their metadata
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            results.append({
                'chunk': self.chunks[idx],
                'metadata': self.metadata[idx],
                'question': self.questions[idx],
                'score': float(distance)
            })
        
        return results