from flask import request, jsonify

from src.main.adapters.chatpro_http_client import ChatProHttpClient
from src.main.domain.entities.conversation_state import ConversationManager
from src.main.domain.usecases.process_webhook_message import ProcessWebhookMessage


class WebhookController:
    def __init__(self):
        self.chatpro_client = ChatProHttpClient()
        self.conversation_manager = ConversationManager()
        self.process_webhook = ProcessWebhookMessage(self.chatpro_client, self.conversation_manager)

    def handle_webhook(self):
        try:
            data = request.get_json()

            if not data:
                return jsonify({"error": "No data received"}), 400

            # Verificar se é uma mensagem recebida
            if data.get('type') == 'received' and data.get('body'):
                result = self.process_webhook.execute(data)
                return jsonify(result), 200

            return jsonify({"status": "acknowledged"}), 200

        except Exception as e:
            print(f"Error processing webhook: {e}")
            return jsonify({"error": "Internal server error"}), 500