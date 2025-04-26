import os
import pickle
import faiss
import numpy as np
from utils.embedder import LocalEmbedder

DB_DIR = "/Users/kshitijpal/Desktop/PhysiAI/img_db"
INDEX_PATH = os.path.join(DB_DIR, "faiss_index.faiss")
METADATA_PATH = os.path.join(DB_DIR, "metadata.pkl")

def load_vector_db():
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def retrieve_image(query, top_k=1):
    embedder = LocalEmbedder()
    query_embedding = embedder.get_embedding(query)
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

    index, metadata = load_vector_db()

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx]['content_path'])
        else:
            results.append(None)

    return results


