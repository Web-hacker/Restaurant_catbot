import json
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS as LC_FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os

# === Step 1: Load the optimized corpus ===
with open("../Structured_data/optimized_corpus.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = data["documents"]
metadata = data["metadata"]

# === Step 2: Load BGE embedding model ===
print("🔄 Loading embedding model...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# === Step 3: Generate normalized embeddings ===
print("🔄 Generating embeddings...")
embeddings = model.encode(
    documents,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

# === Step 4: Convert to LangChain documents ===
print("🔄 Wrapping documents...")
docs = [Document(page_content=text, metadata=meta) for text, meta in zip(documents, metadata)]

# === Step 5: Use LangChain HuggingFace embedding wrapper ===
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# === Step 6: Create FAISS index and save ===
print("💾 Saving FAISS index...")
faiss_path = "faiss_bge_index_optimized"
vectorstore = LC_FAISS.from_documents(docs, embedding_model)
vectorstore.save_local(faiss_path)

print(f"✅ Index saved to `{faiss_path}` with index.faiss and index.pkl.")
