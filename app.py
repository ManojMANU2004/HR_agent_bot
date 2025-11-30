import streamlit as st
import requests

BACKEND_URL = "https://hr-agent-bot.onrender.com/ask"

st.set_page_config(page_title="HR Assistant", page_icon="🤖")
st.title("🤖 HR Assistant Chatbot")
st.write("Ask me anything about HR policies, leaves, benefits, compensation, etc.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Type your question here:")

if st.button("Send") and user_input.strip():
    payload = {"question": user_input.strip()}

    with st.spinner("Thinking..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=60)
            answer = response.json().get("answer", "⚠ No response received.")
        except Exception as e:
            answer = f"⚠ Error contacting backend: {e}"

    st.session_state.history.append(("user", user_input))
    st.session_state.history.append(("bot", answer))

for sender, message in st.session_state.history:
    if sender == "user":
        st.markdown(
            f"<div style='background:#1e88e5;color:white;padding:10px;border-radius:10px;margin:5px 0;'>{message}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background:#eeeeee;color:black;padding:10px;border-radius:10px;margin:5px 0;'>{message}</div>",
            unsafe_allow_html=True,
        )