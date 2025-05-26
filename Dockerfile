FROM python:3.12-slim

# Instalando dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /code

# Copia dependências primeiro
COPY requirements.txt /code/

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do projeto
COPY . /code/

# Comando padrão para produção
CMD ["gunicorn", "farmacia_escola.wsgi:application", "--bind", "0.0.0.0:8000"]

# Para desenvolvimento, altere para:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
