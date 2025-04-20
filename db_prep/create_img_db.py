import os
import os
import pickle
import faiss
import numpy as np
from dotenv import load_dotenv
from tqdm import tqdm
from utils.generate_questions import QuestionGenerator
from utils.embedder import LocalEmbedder
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
IMAGE_DIR = "/Users/kshitijpal/Desktop/PhysiAI/images"
DB_DIR = "/Users/kshitijpal/Desktop/PhysiAI/img_db"
os.makedirs(DB_DIR, exist_ok=True)

INDEX_PATH = os.path.join(DB_DIR, "faiss_index.faiss")
METADATA_PATH = os.path.join(DB_DIR, "metadata.pkl")

def load_images_from_folder(folder_path):
    return [
        os.path.join(folder_path, fname)
        for fname in os.listdir(folder_path)
        if fname.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

def build_image_vector_db():
    qg = QuestionGenerator(api_key=gemini_api_key)
    embedder = LocalEmbedder()  
    image_paths = load_images_from_folder(IMAGE_DIR)

    all_embeddings = []
    metadata = []

    for img_path in tqdm(image_paths, desc="Processing images"):
        try:
            # Generate 3 image-based questions
            questions = []
            for _ in range(3):
                q = qg.generate_image_question(img_path)
                questions.append(q)

            for q in questions:
                embedding = embedder.get_embedding(q)
                all_embeddings.append(embedding)

                metadata.append({
                    "question": q,
                    "type": "image",
                    "source": os.path.basename(img_path),
                    "content_path": img_path
                })

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    # Build and save FAISS index
    dim = len(all_embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(all_embeddings).astype("float32"))
    faiss.write_index(index, INDEX_PATH)

    # Save metadata
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"FAISS index saved at: {INDEX_PATH}")
    print(f"Metadata saved at: {METADATA_PATH}")


# ========== Run ==========
if __name__ == "__main__":
    build_image_vector_db()


