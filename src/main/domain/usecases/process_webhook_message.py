
from src.main.adapters.chatpro_http_client import ChatProHttpClient
from src.main.domain.entities.chat_message import ChatMessage
from src.main.domain.entities.conversation_state import ConversationManager, ConversationState


class ProcessWebhookMessage:
    def __init__(self, chatpro_client: ChatProHttpClient, conversation_manager: ConversationManager):
        self.chatpro_client = chatpro_client
        self.conversation_manager = conversation_manager

    def execute(self, message_data: dict) -> dict:
        try:
            # Extrair número do remetente (remove @c.us)
            from_whatsapp = message_data.get('from', '')
            from_number = from_whatsapp.split('@')[0] if '@' in from_whatsapp else from_whatsapp

            body = message_data.get('body', '').strip()
            message_id = message_data.get('id', '')

            print(f"📩 Mensagem recebida de: {from_number}")
            print(f"💬 Conteúdo: {body}")
            print(f"🆔 ID da mensagem: {message_id}")

            current_state = self.conversation_manager.get_state(from_number)
            print(f"🔍 Estado atual: {current_state}")

            # Processar mensagem baseado no estado
            if current_state == ConversationState.INITIAL:
                return self._handle_initial_state(from_number, message_id)

            elif current_state == ConversationState.MAIN_MENU:
                return self._handle_main_menu(from_number, body, message_id)

            elif current_state == ConversationState.CONSULT_DEBTS:
                return self._handle_consult_debts(from_number, body, message_id)

            elif current_state == ConversationState.PAY_BILL:
                return self._handle_pay_bill(from_number, body, message_id)

            elif current_state == ConversationState.SUPPORT:
                return self._handle_support(from_number, body, message_id)

            else:
                return self._send_message(from_number,
                                          "Estado desconhecido. Digite 'menu' para voltar ao menu principal.",
                                          message_id)

        except Exception as e:
            error_msg = f"❌ Erro ao processar mensagem: {str(e)}"
            print(error_msg)
            return {"status": False, "error": error_msg}

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
        choice = choice.strip()

        if choice == '1':
            self.conversation_manager.set_state(phone_number, ConversationState.CONSULT_DEBTS)
            response = self._send_message(phone_number,
                                          "🔍 Consulta de débitos selecionada. Por favor, digite seu CPF ou CNPJ:",
                                          message_id)
            return response

        elif choice == '2':
            self.conversation_manager.set_state(phone_number, ConversationState.PAY_BILL)
            response = self._send_message(phone_number,
                                          "💳 Pagamento de conta selecionado. Por favor, digite o código do boleto:",
                                          message_id)
            return response

        elif choice == '3':
            self.conversation_manager.set_state(phone_number, ConversationState.SUPPORT)
            response = self._send_message(phone_number,
                                          "👨‍💼 Você será conectado com um atendente em breve. Por favor, aguarde.",
                                          message_id)
            # Aqui você pode integrar com um sistema de tickets ou fila de atendimento
            return response

        elif choice == '4':
            self.conversation_manager.set_state(phone_number, ConversationState.INITIAL)
            response = self._send_message(phone_number, "👋 Obrigado por usar o ZéCobrança! Até logo!", message_id)
            return response

        elif choice.lower() in ['menu', 'voltar', '0']:
            self.conversation_manager.set_state(phone_number, ConversationState.INITIAL)
            return self._handle_initial_state(phone_number, message_id)

        else:
            response = self._send_message(phone_number, "❌ Opção inválida. Por favor, digite 1, 2, 3 ou 4.", message_id)
            return response

    def _handle_consult_debts(self, phone_number: str, document: str, message_id: str) -> dict:
        # Simulação de consulta de débitos
        if document.strip():
            response_msg = f"📋 Consulta para documento: {document}\n\n"
            response_msg += "💸 Débitos encontrados:\n"
            response_msg += "• Conta de luz: R$ 150,00 (vencida)\n"
            response_msg += "• Água: R$ 89,50 (a vencer)\n"
            response_msg += "• Telefone: R$ 120,00 (vencida)\n\n"
            response_msg += "Digite 'menu' para voltar ou '2' para pagar."

            response = self._send_message(phone_number, response_msg, message_id)
            return response
        else:
            response = self._send_message(phone_number, "❌ Por favor, digite um CPF ou CNPJ válido.", message_id)
            return response

    def _handle_pay_bill(self, phone_number: str, barcode: str, message_id: str) -> dict:
        # Simulação de pagamento
        if barcode.strip():
            response_msg = f"💰 Processando pagamento para código: {barcode}\n\n"
            response_msg += "✅ Pagamento realizado com sucesso!\n"
            response_msg += "📅 Data: 01/01/2024\n"
            response_msg += "💳 Valor: R$ 150,00\n"
            response_msg += "🆔 Transação: #123456\n\n"
            response_msg += "Digite 'menu' para voltar ao menu principal."

            response = self._send_message(phone_number, response_msg, message_id)
            self.conversation_manager.set_state(phone_number, ConversationState.MAIN_MENU)
            return response
        else:
            response = self._send_message(phone_number, "❌ Por favor, digite um código de barras válido.", message_id)
            return response

    def _handle_support(self, phone_number: str, message: str, message_id: str) -> dict:
        # Simulação de atendimento
        response_msg = "✅ Sua solicitação foi registrada!\n"
        response_msg += "📞 Um atendente entrará em contato em breve.\n"
        response_msg += "⏰ Tempo médio de espera: 5 minutos\n\n"
        response_msg += "Digite 'menu' para voltar ao menu principal."

        response = self._send_message(phone_number, response_msg, message_id)
        self.conversation_manager.set_state(phone_number, ConversationState.MAIN_MENU)
        return response

    def _send_message(self, phone_number: str, message: str, quoted_message_id: str) -> dict:
        chat_message = ChatMessage(
            number=phone_number,
            message=message,
            quoted_message_id=quoted_message_id
        )
        return self.chatpro_client.send_message(chat_message)