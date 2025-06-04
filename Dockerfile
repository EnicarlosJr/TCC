# Escolher a imagem base
FROM python:3.12-slim

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /code

# Copiar o arquivo requirements.txt
COPY requirements.txt /code/

# Instalar as dependências do Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o restante do código
COPY . /code/

# Definir as variáveis de ambiente
ENV DJANGO_ENV=dev

# Expor a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
