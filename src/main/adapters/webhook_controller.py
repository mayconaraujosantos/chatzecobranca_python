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

            print(f"📨 Webhook recebido: {data}")

            if not data:
                print("❌ Nenhum dado recebido no webhook")
                return jsonify({"error": "No data received"}), 400

            # Verificar se é uma mensagem recebida do ChatPro
            if data.get('type') == 'received' and data.get('body'):
                print("✅ Mensagem recebida válida, processando...")
                result = self.process_webhook.execute(data)
                return jsonify(result), 200

            # Ack de mensagem (confirmação de entrega)
            elif data.get('cmd') == 'ack':
                print(f"✅ ACK recebido para mensagem: {data.get('id')}")
                return jsonify({"status": "acknowledged"}), 200

            else:
                print(f"⚠️  Webhook ignorado: {data.get('type')}")
                return jsonify({"status": "ignored"}), 200

        except Exception as e:
            error_msg = f"❌ Erro no webhook: {str(e)}"
            print(error_msg)
            return jsonify({"error": "Internal server error"}), 500