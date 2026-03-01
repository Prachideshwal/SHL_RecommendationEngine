import faiss
import pickle
import numpy as np
import os
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "embeddings", "faiss_index.bin")
META_PATH = os.path.join(BASE_DIR, "embeddings", "metadata.pkl")

print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading metadata...")
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_assessment_name(url):

    if not url:
        return "Unknown Assessment"

    try:
        # Remove trailing slash
        url = url.rstrip("/")

        # Extract last part
        name = url.split("/")[-1]

        # Clean text
        name = name.replace("-", " ")
        name = name.replace("_", " ")
        name = name.replace("%28", "")
        name = name.replace("%29", "")

        # Remove 'new'
        name = name.replace(" new", "")

        return name.title()

    except Exception:
        return "Unknown Assessment"


def generate_explanation(query, assessment_query):

    query_words = set(query.lower().split())
    assess_words = set(assessment_query.lower().split())

    overlap = query_words.intersection(assess_words)

    if overlap:
        return f"Matched skills: {', '.join(list(overlap)[:5])}"
    else:
        return "Semantic similarity match based on role and skills"


def recommend(user_query, top_k=5):

    query_embedding = model.encode([user_query]).astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        item = metadata[idx]

        similarity_score = float(scores[0][i])

        confidence = round(similarity_score * 100, 2)

        assessment_name = extract_assessment_name(
            item["Assessment_url"]
        )

        explanation = generate_explanation(
            user_query,
            item["Query"]
        )

        results.append({

            "assessment_name": assessment_name,

            "assessment_url": item["Assessment_url"],

            "similarity_score": round(similarity_score, 4),

            "confidence_percentage": confidence,

            "explanation": explanation
        })

    return results