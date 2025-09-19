from flask import Flask

from src.config.settings import settings
from src.main.infra.http.routes import webhook_bp


def create_app():
    app = Flask(__name__)

    # Configurações adicionais para produção
    if not settings.DEBUG:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    # Registrar blueprints
    app.register_blueprint(webhook_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=settings.PORT,
        debug=settings.DEBUG,
        threaded=True  # Melhor performance para múltiplas requisições
    )