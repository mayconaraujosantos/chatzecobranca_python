from flask import Blueprint
from src.main.adapters.webhook_controller import WebhookController

webhook_controller = WebhookController()

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    return webhook_controller.handle_webhook()

@webhook_bp.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}, 200