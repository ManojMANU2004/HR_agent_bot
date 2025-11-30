import streamlit as st
from api import ask  # your FastAPI logic; we'll call ask() function directly
from pydantic import BaseModel

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title="HR Assistant", page_icon="🤖")
st.title("🤖 HR Assistant Chatbot")
st.write("Ask me anything about HR policies, leaves, benefits, etc.")

# -------------------------------
# Session State for Chat History
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Input from User
# -------------------------------
user_input = st.text_input("Type your question here:")

if st.button("Send") and user_input.strip():
    # Create dummy Query model (same as in api.py)
    class Query(BaseModel):
        question: str

    query_model = Query(question=user_input.strip())

    with st.spinner("Thinking..."):
        response = ask(query_model)  # call api.py function directly

    # Add messages to chat history
    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("bot", response["answer"]))

# -------------------------------
# Display Chat History
# -------------------------------
for sender, message in st.session_state.history:
    if sender == "user":
        st.markdown(f'<div style="background:#2563eb;color:white;padding:10px;border-radius:10px;margin:5px 0;">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background:#e5e7eb;color:black;padding:10px;border-radius:10px;margin:5px 0;">{message}</div>', unsafe_allow_html=True)
