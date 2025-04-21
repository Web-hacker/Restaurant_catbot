"""
faiss_index_builder.py
----------------------
Generates a FAISS vector index from structured restaurant & food data using BAAI/bge-base-en-v1.5 embeddings.

- Input: optimized_corpus.json (with `documents` + `metadata`)
- Output: FAISS index (index.faiss + index.pkl) saved to disk


"""

import json
import os
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS as LC_FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# -------------------------------
# Configuration
# -------------------------------
OPTIMIZED_CORPUS_PATH = "../Structured_data/optimized_corpus.json"
INDEX_OUTPUT_DIR = "faiss_bge_index_optimized"
EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"


# -------------------------------
# Step 1: Load Optimized Corpus
# -------------------------------
print("📄 Loading optimized corpus...")
with open(OPTIMIZED_CORPUS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

documents = data["documents"]
metadata = data["metadata"]
assert len(documents) == len(metadata), "Mismatch between documents and metadata!"


# -------------------------------
# Step 2: Load Embedding Model
# -------------------------------
print("🔄 Loading SentenceTransformer model for embeddings...")
sentence_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


# -------------------------------
# Step 3: Generate Normalized Embeddings
# -------------------------------
print("🧠 Generating embeddings (normalized)...")
embeddings = sentence_model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)


# -------------------------------
# Step 4: Wrap LangChain Documents
# -------------------------------
print("📦 Wrapping data into LangChain Document format...")
docs = [
    Document(page_content=text, metadata=meta)
    for text, meta in zip(documents, metadata)
]


# -------------------------------
# Step 5: Create FAISS Index
# -------------------------------
print("⚙️ Creating FAISS index...")
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
vectorstore = LC_FAISS.from_documents(docs, embedding_model)


# -------------------------------
# Step 6: Save Index
# -------------------------------
print(f"💾 Saving FAISS index to `{INDEX_OUTPUT_DIR}`...")
vectorstore.save_local(INDEX_OUTPUT_DIR)

print(f"✅ Index successfully saved! Files created: `{INDEX_OUTPUT_DIR}/index.faiss`, `{INDEX_OUTPUT_DIR}/index.pkl`")
