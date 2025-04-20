project: Zomato RAG Chatbot 🍽️
description: >
  An intelligent chatbot powered by Retrieval-Augmented Generation (RAG),
  which helps users query real-time restaurant and food data scraped from the web.

authors:
  - name: Anubhav Gyanendra Singh
  - org: Gen AI Internship @ Zomato
  - email: anubhav.gyanendra@example.com

architecture:
  embedding_model: BAAI/bge-base-en-v1.5
  llm_model: MBZUAI/LaMini-Flan-T5-783M
  vector_index: FAISS (cosine similarity)
  retrieval_strategy: MMR (Maximal Marginal Relevance)
  response_pipeline: LangChain + HuggingFacePipeline
  UI: Streamlit App with memory + loader + styled cards
  fallback_logic: Manual structured retrieval for list-based or specific queries

features:
  - Real-time food & restaurant query resolution
  - Conversational memory
  - Ambiguity handling
  - RAG fallback with structured filtering
  - Loader animation and user-friendly Streamlit interface
  - Token-safe prompt truncation
  - Manual override for list-style or factual retrieval
  - ConversationalRetrievalChain for memory context

setup:
  clone: |
    git clone https://github.com/your-username/zomato-rag-chatbot.git
    cd zomato-rag-chatbot

  install: |
    pip install -r requirements.txt

  launch: |
    streamlit run app.py

file_structure:
  ├── app.py                    # Streamlit UI
  ├── rag_engine.py            # Retrieval + Generation backend logic
  ├── scraper/                 # Web scraping logic and city-based scrapers
  ├── faiss_bge_index/         # Saved FAISS index and metadata
  ├── optimized_corpus.json    # Cleaned and structured restaurant data
  ├── requirements.txt
  ├── .gitignore
  └── README.md

manual_overrides:
  triggers:
    - restaurant-list
    - menu-list
    - serves-dish-item
  handler: manual_context.py (custom context return logic)

common_questions:
  - "Which restaurants serve Chinese food?"
  - "Show me Jain or vegan options in XYZ city."
  - "Compare KFC and Burger King based on price range."
  - "Does ABC restaurant have butter paneer?"

notes:
  - LaMini-Flan-T5 chosen for balance of performance and inference cost
  - Custom `truncate_prompt()` ensures no overflow errors
  - FAISS index rebuilt on cleaned dataset with cosine normalization

deployment:
  requirements:
    - Python ≥ 3.9
    - Streamlit ≥ 1.28
    - transformers
    - sentence-transformers
    - langchain
    - faiss-cpu
    - BeautifulSoup4
    - requests
    - selenium
    - tqdm
    - nest_asyncio

demo:
  video: "📽️ Add video link here (e.g., YouTube or Loom)"
  interaction_examples:
    - input: "Which restaurants serve under ₹100 dishes?"
      output: "Desi Kitchen, Shiv Sagar"

future_improvements:
  - Switch to Mistral-7B-Instruct (requires GPU setup)
  - Better question rewriting (T5 or Rewriter LLM)
  - Query clustering for FAQs
  - Fine-tuned dish tag embeddings
  - Dockerize and deploy on Streamlit Cloud or HuggingFace Spaces

license: MIT
