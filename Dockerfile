# Use a imagem oficial do Python
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar pipenv
RUN pip install --no-cache-dir pipenv

# Copiar Pipfile e Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Instalar dependências do projeto
RUN pipenv install --system --deploy

# Copiar o código fonte
COPY . .

# Expor a porta que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]