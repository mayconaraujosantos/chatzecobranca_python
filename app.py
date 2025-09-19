from flask import Flask, request

from src.config.settings import settings
import logging

from src.main.infra.http.routes import webhook_bp


def create_app():
    app = Flask(__name__)

    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Configurações adicionais para produção
    if not settings.DEBUG:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    else:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    # Registrar blueprints
    app.register_blueprint(webhook_bp)

    @app.before_request
    def log_request():
        if request.path == '/webhook':
            logger.info(f"📍 Request recebido: {request.method} {request.path}")

    return app


if __name__ == '__main__':
    app = create_app()
    print(f"🚀 Iniciando ZéCobrança na porta {settings.PORT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    print(f"🌐 ChatPro Instance: {settings.CHATPRO_INSTANCE_ID}")

    app.run(
        host='0.0.0.0',
        port=settings.PORT,
        debug=settings.DEBUG,
        threaded=True
    )