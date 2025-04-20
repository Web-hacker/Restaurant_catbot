
import os
import traceback
from transformers import pipeline, AutoTokenizer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from manual_context import give_custom_context as custom_context

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"



# -------------------------------
# Load FAISS Vector Index Safely
# -------------------------------
try:
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    db = FAISS.load_local("data/faiss_bge_index", embedding_model, allow_dangerous_deserialization=True)
except Exception as e:
    print("❌ Failed to load FAISS index. Please ensure it's built and saved properly.")
    raise e

retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10}
)

# -------------------------------
# Load LLM Pipeline
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
    device=-1  # CPU
)

llm = HuggingFacePipeline(pipeline=hf_pipeline)

# -------------------------------
# Prompt Template
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
def truncate_prompt(prompt, tokenizer, max_tokens=1024):
    tokens = tokenizer.encode(prompt, max_length=max_tokens, truncation=True)
    return tokenizer.decode(tokens, skip_special_tokens=True)

# -------------------------------
# Main CLI Bot
# -------------------------------
#print("🍽️ Welcome to the Zomato Chatbot! Type 'exit' to quit.")
def get_rag_response(query):
    user_input = query.strip()
    
    if "restaurant-list" in user_input.lower() or "menu-list" in user_input.lower() or "serves-dish-item" in user_input.lower():
        return custom_context(user_input)
    
    if not user_input:
        return "Please ask something meaningful."
        

    try:
        # Retrieve relevant documents
        docs = retriever.invoke(user_input)
        if not docs or all(not doc.page_content.strip() for doc in docs):
            response = "Sorry, I couldn’t find relevant info right now."
            

        # Merge context and generate prompt
        context = "\n".join([doc.page_content for doc in docs])
        raw_prompt = prompt_template.format(context=context, question=user_input)
        safe_prompt = truncate_prompt(raw_prompt, tokenizer)

        # Get response from LLM
        result = hf_pipeline(safe_prompt)
        response = result[0]["generated_text"].strip()

        # Validate response
        if not response or any(word in response.lower() for word in ["not available", "don't know", "sorry"]):
            response = "Sorry, I couldn’t find a confident answer."
        

        return response

    except Exception as e:
        return "Oops! Something went wrong."
    

