import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class VectorDBManager:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.metadata = []
        self.questions = []

    def create_index(self, questions, chunks, metadata, batch_size=32):
        self.chunks = chunks
        self.metadata = metadata
        self.questions = questions

        embeddings = self.model.encode(questions, batch_size=batch_size, convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def save_index(self, path):
        if self.index is not None:
            faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path)

    def save_data(self, path):
        with open(path, "wb") as f:
            pickle.dump({
                "chunks": self.chunks,
                "metadata": self.metadata,
                "questions": self.questions
            }, f)

    def load_data(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.chunks = data["chunks"]
            self.metadata = data["metadata"]
            self.questions = data["questions"]

    def query(self, query_text, top_k=3):
        if self.index is None:
            raise ValueError("Index not created or loaded")

        query_vector = self.model.encode([query_text], convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, distance in zip(indices[0], distances[0]):
            results.append({
                'chunk': self.chunks[idx],
                'metadata': self.metadata[idx],
                'question': self.questions[idx],
                'score': float(distance)
            })

        return results
