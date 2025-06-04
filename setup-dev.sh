#!/bin/bash

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" &>/dev/null
}

echo "🔧 Iniciando ambiente de desenvolvimento local..."

# 1. Defina o ambiente
export DJANGO_ENV=dev
export DJANGO_SETTINGS_MODULE=farmacia_escola.settings
echo "📁 Ambiente definido: DJANGO_ENV=dev"

# 2. Ativa o .env.dev
ENV_FILE=".env.dev"
if [ ! -f "$ENV_FILE" ]; then
  echo "❌ Arquivo $ENV_FILE não encontrado. Crie um arquivo com as variáveis necessárias."
  exit 1
fi
echo "🔐 Carregando variáveis de ambiente do $ENV_FILE..."
set -o allexport
source "$ENV_FILE"
set +o allexport

# 3. Verificar se python3 e pip estão instalados
if ! command_exists python3; then
    echo "❌ Python 3 não encontrado. Instale o Python 3."
    exit 1
fi
if ! command_exists pip; then
    echo "❌ Pip não encontrado. Instale o Pip."
    exit 1
fi

# 4. Cria o ambiente virtual se não existir
if [ ! -d "env" ]; then
  echo "🐍 Criando ambiente virtual..."
  python3 -m venv env || {
    echo "❌ Falha ao criar o ambiente virtual."
    exit 1
  }
fi

# 5. Ativa o ambiente virtual
source env/bin/activate

# 6. Instala dependências
echo "📦 Instalando dependências do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt || {
  echo "❌ ERRO: Falha ao instalar as dependências."
  exit 1
}

# 7. Verifica PostgreSQL
echo "📡 Verificando PostgreSQL local..."
if ! systemctl is-active --quiet postgresql; then
  echo "⚠️ PostgreSQL não está ativo. Tentando iniciar..."
  sudo systemctl start postgresql || {
    echo "❌ Falha ao iniciar o PostgreSQL. Verifique manualmente."
    exit 1
  }
fi
echo "✅ PostgreSQL está rodando."

# 8. Cria banco se necessário
echo "🛠️ Verificando existência do banco '${DB_NAME}'..."
if sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1; then
  echo "ℹ️ Banco '${DB_NAME}' já existe."
else
  echo "➕ Criando banco '${DB_NAME}'..."
  sudo -u postgres createdb -E UTF8 -T template1 "$DB_NAME" || {
    echo "❌ Erro ao criar o banco de dados."
    exit 1
  }
fi

# 9. Apaga migrações antigas
echo "🧹 Limpando migrações antigas..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 10. Cria migrações (login primeiro!)
echo "📐 Criando novas migrações..."
python manage.py makemigrations login
python manage.py makemigrations || {
  echo "❌ Erro ao criar migrações. Verifique se há problemas no seu código."
  exit 1
}

# 11. Aplica migrações
echo "📦 Aplicando migrações..."
python manage.py migrate || {
  echo "❌ ERRO: Falha ao aplicar migrações. Verifique o settings.py e banco."
  exit 1
}

# 12. Cria superusuário se não existir
echo "👤 Verificando superusuário '${SUPERUSER_NAME}'..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${SUPERUSER_NAME}').exists():
    User.objects.create_superuser('${SUPERUSER_NAME}', '${SUPERUSER_EMAIL}', '${SUPERUSER_PASSWORD}')
    print("✅ Superusuário '${SUPERUSER_NAME}' criado.")
else:
    print("ℹ️ Superusuário '${SUPERUSER_NAME}' já existe.")
EOF

# 13. Coleta arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || {
  echo "❌ Erro ao coletar arquivos estáticos."
  exit 1
}

# 14. Inicia servidor
echo "🚀 Iniciando servidor de desenvolvimento: http://127.0.0.1:8000/"
python manage.py runserver
echo "✅ Ambiente de desenvolvimento configurado com sucesso!"
