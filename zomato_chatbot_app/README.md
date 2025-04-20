# 🍽️ Zomato RAG Chatbot

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

## 🗂️ Project Structure

Zomato-RAG-Chatbot/
│
├── data/                          # Optional: contains FAISS index or corpus files
│   ├── faiss_bge_index/          
│   └── optimized_corpus.json     
│
├── rag_engine.py                 # Core retrieval + generation logic
├── app.py                        # Streamlit front-end
├── manual_context.py             # Custom structured rule-based retrieval
├── requirements.txt              # Dependencies
├── README.md                     # Project documentation
└── .gitignore                    # Ignore unnecessary files


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


2. Create and activate a virtual environment

```bash
conda create -n zomato-chatbot python=3.10
conda activate zomato-chatbot

3. Install required packages
bash

pip install -r requirements.txt
4. (Optional) Rebuild FAISS Index
If not using the saved index:

bash

python build_faiss_index.py
💬 Run the Streamlit App
bash
streamlit run app.py
This launches the chatbot interface in your browser. Ask questions like:

“Which restaurants serve Jain food?”

“Does ABC Restaurant have gluten-free items?”

“Compare prices of biryani dishes in Kanpur”

💡 Sample Queries Supported
Menu item lookup

Price range by dish/cuisine

Vegetarian / vegan options

Restaurant rating comparison

Delivery times

Structured queries: "restaurant-list::city" or "serves-dish-item::paneer butter masala"

🔧 Tech Stack
🐍 Python 3.10

🧠 LangChain + Hugging Face Transformers

💾 FAISS for dense vector retrieval

🌐 Streamlit for UI

📈 Future Improvements
Upgrade to Mistral-7B or LLaMA models with more memory

Add multilingual support

Advanced query rewriting

Fine-tuning LaMini-Flan for improved coherence

Real-time scraping for live menu updates

📄 License
This project is open-sourced under the MIT License.

👨‍💻 Maintainer
Developed by Anubhav Gyanendra Singh

Internship Assignment for Zomato Generative AI Track

🙌 Acknowledgements
Hugging Face 🤗

LangChain Team

BAAI & MBZUAI research teams

Zomato for the internship opportunity