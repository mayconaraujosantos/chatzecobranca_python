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

            # O webhook do ChatPro é um array [tipo, dados]
            if isinstance(data, list) and len(data) == 2:
                event_type = data[0]
                event_data = data[1]

                print(f"🎯 Tipo de evento: {event_type}")
                print(f"📊 Dados do evento: {event_data}")

                # Mensagem recebida
                if event_type == "Msg" and event_data.get('body'):
                    print("✅ Mensagem recebida válida, processando...")

                    # Extrair dados na estrutura CORRETA
                    message_data = {
                        'type': 'received',
                        'from': event_data.get('from'),
                        'body': event_data.get('body'),
                        'id': event_data.get('id'),
                        'timestamp': event_data.get('t'),
                        'chatId': event_data.get('chatId'),
                        'to': event_data.get('to'),
                        'ack': event_data.get('ack'),
                        'cmd': event_data.get('cmd'),
                        'sender': event_data.get('sender', {})
                    }

                    result = self.process_webhook.execute(message_data)
                    return jsonify(result), 200

                # Confirmação de entrega (ACK)
                elif event_type == "Cmd" and event_data.get('cmd') == 'ack':
                    print(f"✅ ACK recebido para mensagem: {event_data.get('id')}")
                    return jsonify({"status": "acknowledged"}), 200

                else:
                    print(f"⚠️  Evento ignorado: {event_type} - {event_data.get('cmd')}")
                    return jsonify({"status": "ignored"}), 200

            else:
                print(f"❌ Formato de webhook inválido: {type(data)}")
                return jsonify({"error": "Invalid webhook format"}), 400

        except Exception as e:
            error_msg = f"❌ Erro no webhook: {str(e)}"
            print(error_msg)
            return jsonify({"error": "Internal server error"}), 500