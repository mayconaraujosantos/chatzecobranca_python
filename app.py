import logging

from flask import Flask, request

from src.config.settings import settings
from src.main.infra.http.routes import webhook_bp


def create_app():
    app = Flask(__name__)

    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Configurações
    if not settings.DEBUG:
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
    else:
        app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    # Registrar blueprints
    app.register_blueprint(webhook_bp)

    @app.before_request
    def log_request_info():
        if request.path == "/webhook":
            logger.info(f"📍 Webhook request: {request.method} {request.path}")
            if request.is_json:
                logger.info(f"📦 Request body: {request.get_json()}")

    @app.after_request
    def log_response_info(response):
        if request.path == "/webhook":
            logger.info(f"📤 Response: {response.status_code}")
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    print(f"🚀 Iniciando ZéCobrança na porta {settings.PORT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    print(f"🌐 ChatPro Instance: {settings.CHATPRO_INSTANCE_ID}")
    print(
        f"🔑 API Key: {'*' * len(settings.CHATPRO_API_KEY) if settings.CHATPRO_API_KEY else 'Not set'}"
    )

    app.run(host="0.0.0.0", port=settings.PORT, debug=settings.DEBUG, threaded=True)
