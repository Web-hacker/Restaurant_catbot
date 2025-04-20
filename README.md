# 🍽️ Restaurant RAG Chatbot

This project is a powerful Generative AI chatbot that lets users ask natural language questions about restaurants, menus, cuisines, and pricing using Retrieval-Augmented Generation (RAG). It combines intelligent vector search using FAISS with Hugging Face transformer models to provide accurate, context-based answers.

---

## 📌 Key Features

- ✅ Retrieval-Augmented Generation (RAG) pipeline
- 🔍 Embedding via `BAAI/bge-base-en-v1.5`
- 🧠 Local answer generation with `MBZUAI/LaMini-Flan-T5-783M`
- 🧾 Token-safe prompt handling
- 🧩 Manual structured fallback for better list/lookup-type answers
- 🧠 Streamlit interface with conversation memory and markdown rendering


---

## 🚀 How It Works

1. **User asks a question**
2. **Retriever** uses FAISS (built on BGE embeddings) to fetch relevant restaurant/menu data
3. **LLM (LaMini-Flan-T5)** generates a natural language response using a custom prompt template
4. If a query is a known structured type, a fallback **manual retriever** answers from JSON directly

---

## 🧠 Models Used

| Component        | Model                                  |
|------------------|----------------------------------------|
| Embeddings       | `BAAI/bge-base-en-v1.5` (Cosine-based) |
| LLM (Answer Gen) | `MBZUAI/LaMini-Flan-T5-783M` (local)   |

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/zomato-rag-chatbot.git
cd zomato-rag-chatbot
```
### 2. Create and activate a virtual environment

```bash
conda create -n zomato-chatbot python=3.10
conda activate zomato-chatbot
```
### 3. Install required packages

```bash
pip install -r requirements.txt
```
### 4. (Optional) Rebuild FAISS Index

If not using the saved index:

```bash
python build_faiss_index.py
```

---

## 💬 Run the Streamlit App

```bash
streamlit run app.py
```
This launches the chatbot interface in your browser. Ask questions like:

1. “Which restaurants serve Chinese food?”

2. “Does ABC Restaurant have veg items?”

3. “Compare prices of biryani at restaurant ABC and restaurant XYZ”

---

## Sample Queries Supported

1. Menu item lookup

2. Price of dish/cuisine

3. Vegetarian / vegan options

4. Restaurant rating comparison

5. Delivery times

6. Structured queries: "restaurant-list::city" or "serves-dish-item::paneer butter masala"


---

## Tech Stack
1. 🐍 Python 3.10

2. 🧠 LangChain + Hugging Face Transformers

3. 💾 FAISS for dense vector retrieval

4. 🌐 Streamlit for UI

---

## Future Improvements

1. Upgrade to Mistral-7B or LLaMA models with more memory

2. Add multilingual support

3. Advanced query rewriting

4. Fine-tuning LaMini-Flan for improved coherence

5. Real-time scraping for live menu updates

## 📄 License
This project is open-sourced under the MIT License.

## 👨‍💻 Maintainer
Developed by Anubhav Gyanendra Singh


## 🙌 Acknowledgements
Hugging Face 🤗

LangChain Team

BAAI & MBZUAI research teams



