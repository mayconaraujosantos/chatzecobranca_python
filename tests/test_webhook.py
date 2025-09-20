import pytest

from src.main.domain.entities.conversation_state import (ConversationManager,
                                                         ConversationState)


def test_conversation_manager():
    manager = ConversationManager()

    # Testar estado inicial
    assert manager.get_state("5511999999999") == ConversationState.INITIAL

    # Testar mudança de estado
    manager.set_state("5511999999999", ConversationState.MAIN_MENU)
    assert manager.get_state("5511999999999") == ConversationState.MAIN_MENU

    # Testar atualização de última mensagem
    manager.update_last_message("5511999999999", "Olá")
    conversation = manager.conversations["5511999999999"]
    assert conversation.last_message == "Olá"


def test_conversation_state_enum():
    assert ConversationState.INITIAL.value == "initial"
    assert ConversationState.MAIN_MENU.value == "main_menu"
    assert ConversationState.CONSULT_DEBTS.value == "consult_debts"
