import streamlit as st
import requests

# ---------------- CHATBOT CLASS ----------------
class MultilingualChatbot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai/v1/chat/completions"
        self.headers = {
            "api-subscription-key": api_key,
            "Content-Type": "application/json",
        }

    def get_chat_response(self, user_input: str):
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={
                "model": "sarvam-m",
                "messages": [{"role": "user", "content": user_input}],
            },
        )

        if response.status_code != 200:
            return f"❌ Error: {response.text}"

        return response.json()["choices"][0]["message"]["content"]


# ---------------- STREAMLIT UI ----------------

st.title("🤖 Sarvam Chatbot")

# 🔑 API KEY INPUT
api_key = st.text_input("Enter API Key", type="password")

# 💬 User input
user_input = st.text_input("Ask something")

# ▶️ Button
if st.button("Send"):
    if not api_key:
        st.warning("Enter API Key")
    elif not user_input:
        st.warning("Enter message")
    else:
        bot = MultilingualChatbot(api_key)
        reply = bot.get_chat_response(user_input)
        st.write("### 🤖 Bot:")
        st.write(reply)