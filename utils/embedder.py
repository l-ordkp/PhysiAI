from sentence_transformers import SentenceTransformer

# Load the model only once at the module level
_model = SentenceTransformer("all-MiniLM-L6-v2")

class LocalEmbedder:
    def __init__(self):
        """
        Use a hardcoded local embedding model (all-MiniLM-L6-v2).
        """
        self.model = _model  # Reuse the already-loaded model

    def get_embedding(self, text):
        """
        Generate embedding for the given text.

        Args:
            text (str): Input text
        Returns:
            list[float]: Embedding vector
        """
        return self.model.encode(text).tolist()
