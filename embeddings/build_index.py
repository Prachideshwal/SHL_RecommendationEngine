import pandas as pd
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/Gen_AI Dataset.xlsx"
INDEX_PATH = "embeddings/faiss_index.bin"
META_PATH = "embeddings/metadata.pkl"

print("Loading dataset...")
df = pd.read_excel(DATA_PATH)

# Validate columns
required = ["Query", "Assessment_url"]
for col in required:
    if col not in df.columns:
        raise Exception(f"Missing required column: {col}")

# Create embedding text
df["combined_text"] = df["Query"].astype(str)

texts = df["combined_text"].tolist()

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)

# Normalize embeddings for cosine similarity
faiss.normalize_L2(embeddings)

index.add(embeddings)

os.makedirs("embeddings", exist_ok=True)

faiss.write_index(index, INDEX_PATH)

with open(META_PATH, "wb") as f:
    pickle.dump(df.to_dict("records"), f)

print("Index built successfully!")