import logging

from flask import jsonify, request

from src.main.adapters.chatpro_http_client import ChatProHttpClient
from src.main.domain.entities.conversation_state import ConversationManager
from src.main.domain.usecases.process_webhook_message import \
    ProcessWebhookMessage

logger = logging.getLogger(__name__)


class WebhookController:
    def __init__(self):
        self.chatpro_client = ChatProHttpClient()
        self.conversation_manager = ConversationManager()
        self.process_webhook = ProcessWebhookMessage(
            self.chatpro_client, self.conversation_manager
        )

    def handle_webhook(self):
        try:
            data = request.get_json()

            logger.info(f"📨 Webhook recebido: {data}")

            if not data:
                logger.warning("❌ Nenhum dado recebido no webhook")
                return jsonify({"error": "No data received"}), 400

            webhook_type = data.get("Type")

            # Mensagem recebida (nova estrutura do ChatPro)
            if webhook_type == "receveid_message" and data.get("Body", {}).get("Text"):
                logger.info("✅ Mensagem recebida válida, processando...")

                body_data = data.get("Body", {})
                info_data = body_data.get("Info", {})

                # Extrair dados na estrutura CORRETA do seu ChatPro
                message_data = {
                    "type": "received",
                    "from": info_data.get("RemoteJid", "").replace(
                        "@s.whatsapp.net", "@c.us"
                    ),
                    "body": body_data.get("Text", ""),
                    "id": info_data.get("Id", ""),
                    "timestamp": info_data.get("Timestamp", 0),
                    "pushName": info_data.get("PushName", ""),
                    "remoteJid": info_data.get("RemoteJid", ""),
                    "senderJid": info_data.get("SenderJid", ""),
                    "fromMe": info_data.get("FromMe", False),
                }

                logger.info(f"📝 Dados extraídos: {message_data}")
                result = self.process_webhook.execute(message_data)
                return jsonify(result), 200

            # Outros tipos de webhook (implementar conforme necessidade)
            elif webhook_type in ["ack_message", "status_message"]:
                logger.info(f"📊 Webhook de {webhook_type} recebido")
                return jsonify({"status": f"{webhook_type}_acknowledged"}), 200

            else:
                logger.warning(
                    f"⚠️  Webhook ignorado (tipo desconhecido): {webhook_type}"
                )
                return jsonify({"status": "ignored"}), 200

        except Exception as e:
            error_msg = f"❌ Erro no webhook: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return jsonify({"error": "Internal server error"}), 500
