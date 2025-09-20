import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class Settings:
    CHATPRO_BASE_URL = os.getenv("CHATPRO_BASE_URL", "https://v5.chatpro.com.br")
    CHATPRO_INSTANCE_ID = os.getenv("CHATPRO_INSTANCE_ID", "chatpro-zbeypgdzf1")
    CHATPRO_API_KEY = os.getenv("CHATPRO_API_KEY", "aa4383ebaa5bd78d679f56b5288797bb")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    RAILWAY_ENVIRONMENT = os.getenv("RAILWAY_ENVIRONMENT", "development")


settings = Settings()
