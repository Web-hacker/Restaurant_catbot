
import streamlit as st
from rag_engine import get_rag_response  

st.set_page_config(page_title="Zomato RAG Chatbot", page_icon="🍽️")

st.title("🍽️ Zomato RAG Chatbot")
st.markdown("Ask anything about restaurants, menus, cuisines, etc.")

# Initialize state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# HTML styling
def user_card(text):
    return f"""
    <div style="background-color:#f0f2f6;padding:10px;border-radius:10px;margin-bottom:10px;">
        <b style="color:#1f77b4;">You:</b> {text}
    </div>
    """

def bot_card(text):
    return f"""
    <div style="background-color:#d2f8d2;padding:10px;border-radius:10px;margin-bottom:15px;">
        <b style="color:#2c7a7b;">Bot:</b> {text}
    </div>
    """

# Input area
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here 👇", placeholder="e.g. Show me restaurants serving vegan dishes")
    submitted = st.form_submit_button("➤ Send", use_container_width=True)

# Step 1: Add user message immediately
if submitted and user_input:
    # Append user message with placeholder for bot
    st.session_state.chat_history.append({"user": user_input, "bot": "⏳ Thinking..."})
    st.rerun()


# Step 2: Replace placeholder with actual bot response
for message in st.session_state.chat_history:
    st.markdown(user_card(message["user"]), unsafe_allow_html=True)
    if message["bot"] == "⏳ Thinking...":
        response = get_rag_response(message["user"])
        message["bot"] = response or "Sorry, I couldn’t find a confident answer."
        st.rerun()
    st.markdown(bot_card(message["bot"]), unsafe_allow_html=True)
