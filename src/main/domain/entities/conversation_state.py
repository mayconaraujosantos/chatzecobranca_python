from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ConversationState(Enum):
    INITIAL = "initial"
    MAIN_MENU = "main_menu"
    CONSULT_DEBTS = "consult_debts"
    PAY_BILL = "pay_bill"
    SUPPORT = "support"


@dataclass
class UserConversation:
    phone_number: str
    state: ConversationState
    last_message: Optional[str] = None
    data: Optional[dict] = None


class ConversationManager:
    def __init__(self):
        self.conversations = {}

    def get_state(self, phone_number: str) -> ConversationState:
        if phone_number not in self.conversations:
            return ConversationState.INITIAL
        return self.conversations[phone_number].state

    def set_state(self, phone_number: str, state: ConversationState, data: dict = None):
        if phone_number not in self.conversations:
            self.conversations[phone_number] = UserConversation(
                phone_number=phone_number, state=state, data=data or {}
            )
        else:
            self.conversations[phone_number].state = state
            if data:
                self.conversations[phone_number].data = data

    def update_last_message(self, phone_number: str, message: str):
        if phone_number in self.conversations:
            self.conversations[phone_number].last_message = message
