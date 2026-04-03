
import requests

from typing import List, Dict, Any


class MultilingualChatbot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sarvam.ai/v1/chat/completions"
        self.translate_url = "https://api.sarvam.ai/translate"

        # ✅ FIXED HEADERS
        self.headers = {
            "api-subscription-key": api_key,
            "Content-Type": "application/json",
        }

        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 5

    def detect_language(self, text: str) -> str:
        for char in text:
            code = ord(char)
            if 0x0900 <= code <= 0x097F:
                return "hindi"
            elif 0x0B80 <= code <= 0x0BFF:
                return "tamil"
            elif 0x0C00 <= code <= 0x0C7F:
                return "telugu"
        return "english"

    def get_chat_response(self, user_input: str):
        self.conversation_history.append({"role": "user", "content": user_input})

        messages = [
            {
                "role": "system",
                "content": "Reply in same language as user."
            }
        ]

        messages.extend(self.conversation_history[-self.max_history:])

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={
                "model": "sarvam-m",
                "messages": messages
            }
        )

        print("Status:", response.status_code)
        print("Raw:", response.text[:300])

        if response.status_code != 200:
            return "API Error"

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        self.conversation_history.append(
            {"role": "assistant", "content": reply}
        )

        return reply


# ---------------- RUN IN COLAB ----------------

api_key = "sk_plv9dmg5_nSBp9Pn76vprkbtVf0PZ8yPG"

bot = MultilingualChatbot(api_key)

# Single test (no loop)
response = bot.get_chat_response("Hello, how are you?")
print("\nBot:", response)
