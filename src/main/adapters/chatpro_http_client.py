import json
import logging

import requests

from src.config.settings import settings
from src.main.domain.entities.chat_message import ChatMessage

logger = logging.getLogger(__name__)


class ChatProHttpClient:
    def __init__(self):
        self.base_url = (
            f"{settings.CHATPRO_BASE_URL}/{settings.CHATPRO_INSTANCE_ID}/api/v1"
        )
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": settings.CHATPRO_API_KEY,
        }

    def send_message(self, chat_message: ChatMessage) -> dict:
        url = f"{self.base_url}/send_message"
        payload = {"number": chat_message.number, "message": chat_message.message}

        # Adicionar quoted_message_id se existir
        if chat_message.quoted_message_id:
            payload["quoted_message_id"] = chat_message.quoted_message_id

        logger.info(f"📤 Enviando mensagem para ChatPro: {url}")
        logger.debug(f"📝 Payload: {json.dumps(payload, ensure_ascii=False)}")
        logger.debug(f"🔑 Headers: {json.dumps(self.headers, ensure_ascii=False)}")

        try:
            response = requests.post(
                url, json=payload, headers=self.headers, timeout=30
            )

            logger.info(
                f"📥 Resposta do ChatPro: {response.status_code} - {response.text}"
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            error_msg = f"❌ Erro ao enviar mensagem para ChatPro: {str(e)}"
            if hasattr(e, "response") and e.response is not None:
                error_msg += f" - Response: {e.response.text}"
            logger.error(error_msg)
            return {"status": False, "error": error_msg}
