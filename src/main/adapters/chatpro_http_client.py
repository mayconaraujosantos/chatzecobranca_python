import requests

from src.config.settings import settings
from src.main.domain.entities.chat_message import ChatMessage


class ChatProHttpClient:
    def __init__(self):
        self.base_url = f"{settings.CHATPRO_BASE_URL}/{settings.CHATPRO_INSTANCE_ID}/api/v1"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": settings.CHATPRO_API_KEY
        }

    def send_message(self, chat_message: ChatMessage) -> dict:
        url = f"{self.base_url}/send_message"
        payload = chat_message.to_dict()

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to ChatPro: {e}")
            return {"status": False, "error": str(e)}