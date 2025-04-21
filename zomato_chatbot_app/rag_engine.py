"""
rag_engine.py
-------------
Core logic for the Zomato RAG chatbot.

Responsibilities:
- Loads FAISS index created with BAAI/bge-base-en-v1.5 embeddings.
- Retrieves context using MMR search strategy.
- Generates response using MBZUAI/LaMini-Flan-T5-783M LLM via Hugging Face pipeline.
- Fallbacks to structured JSON lookup (manual_context.py) for specific types of list-based questions.


"""

import os
import traceback
from transformers import pipeline, AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from manual_context import give_custom_context as custom_context

# -------------------------------
# Environment Setup
# -------------------------------
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"  # Avoid ONEDNN conflicts
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disable tokenizer warnings

# -------------------------------
# Load FAISS Vector Index
# -------------------------------
try:
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    db = FAISS.load_local("../faiss_bge_index", embedding_model, allow_dangerous_deserialization=True)
except Exception as e:
    print("❌ Failed to load FAISS index. Please ensure it's built and saved properly.")
    raise e

# Define retriever with MMR
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10}
)

# -------------------------------
# Load Hugging Face LLM Pipeline
# -------------------------------
tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-783M")
hf_pipeline = pipeline(
    "text2text-generation",
    model="MBZUAI/LaMini-Flan-T5-783M",
    tokenizer=tokenizer,
    max_new_tokens=512,
    truncation=True,
    do_sample=True,
    temperature=0.3,
    device=-1  # CPU inference
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# -------------------------------
# Prompt Template Definition
# -------------------------------
prompt_template = PromptTemplate.from_template("""
You are a helpful assistant for a food recommendation app.
Use the following context to answer the question.
Answer in list or in brief whenever asked.                                               
If the answer cannot be found, say politely that it's not available.

Context:
{context}

Question: {question}

Answer:
""")

# -------------------------------
# Token-safe prompt formatting
# -------------------------------
def truncate_prompt(prompt: str, tokenizer, max_tokens: int = 1024) -> str:
    """
    Ensure the prompt is within the LLM's token limit.
    """
    tokens = tokenizer.encode(prompt, max_length=max_tokens, truncation=True)
    return tokenizer.decode(tokens, skip_special_tokens=True)

# -------------------------------
# Main RAG Handler
# -------------------------------
def get_rag_response(query: str) -> str:
    """
    Core retrieval-augmented generation logic.

    Args:
        query (str): User input

    Returns:
        str: Model-generated answer or fallback message
    """
    user_input = query.strip()

    # Manual override for predefined structured lookups
    if any(key in user_input.lower() for key in ["restaurant-list", "menu-list", "serves-dish-item"]):
        return custom_context(user_input)

    if not user_input:
        return "Please ask something meaningful."

    try:
        # Step 1: Retrieve documents using FAISS retriever
        docs = retriever.invoke(user_input)
        if not docs or all(not doc.page_content.strip() for doc in docs):
            return "Sorry, I couldn’t find relevant info right now."

        # Step 2: Format prompt with context and question
        context = "\n".join([doc.page_content for doc in docs])
        raw_prompt = prompt_template.format(context=context, question=user_input)
        safe_prompt = truncate_prompt(raw_prompt, tokenizer)

        # Step 3: Get answer from LLM
        result = hf_pipeline(safe_prompt)
        response = result[0]["generated_text"].strip()

        # Step 4: Final fallback check
        if not response or any(phrase in response.lower() for phrase in ["not available", "don't know", "sorry"]):
            return "Sorry, I couldn’t find a confident answer."

        return response

    except Exception as e:
        print("❌ Exception in get_rag_response:")
        traceback.print_exc()
        return "Oops! Something went wrong while processing your request."
