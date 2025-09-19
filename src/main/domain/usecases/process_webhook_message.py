
from src.main.adapters.chatpro_http_client import ChatProHttpClient
from src.main.domain.entities.chat_message import ChatMessage
from src.main.domain.entities.conversation_state import ConversationManager, ConversationState


class ProcessWebhookMessage:
    def __init__(self, chatpro_client: ChatProHttpClient, conversation_manager: ConversationManager):
        self.chatpro_client = chatpro_client
        self.conversation_manager = conversation_manager

    def execute(self, message_data: dict) -> dict:
        from_number = message_data.get('from', '').split('@')[0]
        body = message_data.get('body', '').strip().lower()
        message_id = message_data.get('id', '')

        current_state = self.conversation_manager.get_state(from_number)

        if current_state == ConversationState.INITIAL:
            return self._handle_initial_state(from_number, message_id)

        elif current_state == ConversationState.MAIN_MENU:
            return self._handle_main_menu(from_number, body, message_id)

        # Implementar outros estados conforme necessário

        return self._send_message(from_number, "Opção inválida. Por favor, escolha uma opção válida.", message_id)

    def _handle_initial_state(self, phone_number: str, message_id: str) -> dict:
        welcome_message = """
🤖 Olá! Bem-vindo ao ZéCobrança!

Escolha uma opção:
1️⃣ Consultar débitos
2️⃣ Pagar conta  
3️⃣ Falar com atendente
4️⃣ Sair

Digite o número da opção desejada:
        """

        self.conversation_manager.set_state(phone_number, ConversationState.MAIN_MENU)
        return self._send_message(phone_number, welcome_message, message_id)

    def _handle_main_menu(self, phone_number: str, choice: str, message_id: str) -> dict:
        if choice == '1':
            self.conversation_manager.set_state(phone_number, ConversationState.CONSULT_DEBTS)
            return self._send_message(phone_number, "🔍 Consulta de débitos selecionada. Em desenvolvimento...",
                                      message_id)
        elif choice == '2':
            self.conversation_manager.set_state(phone_number, ConversationState.PAY_BILL)
            return self._send_message(phone_number, "💳 Pagamento de conta selecionado. Em desenvolvimento...",
                                      message_id)
        elif choice == '3':
            self.conversation_manager.set_state(phone_number, ConversationState.SUPPORT)
            return self._send_message(phone_number, "👨‍💼 Falar com atendente selecionado. Em desenvolvimento...",
                                      message_id)
        elif choice == '4':
            self.conversation_manager.set_state(phone_number, ConversationState.INITIAL)
            return self._send_message(phone_number, "👋 Obrigado por usar o ZéCobrança! Até logo!", message_id)
        else:
            return self._send_message(phone_number, "❌ Opção inválida. Por favor, digite 1, 2, 3 ou 4.", message_id)

    def _send_message(self, phone_number: str, message: str, quoted_message_id: str) -> dict:
        chat_message = ChatMessage(
            number=phone_number,
            message=message,
            quoted_message_id=quoted_message_id
        )
        return self.chatpro_client.send_message(chat_message)