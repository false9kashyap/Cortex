from sentence_transformers import SentenceTransformer


# Load transformer only once

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)