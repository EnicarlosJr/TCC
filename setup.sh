#!/bin/bash

echo "✅ Iniciando setup automático do Sistema Farmácia Escola..."

# 1. Cria o arquivo .env a partir do .env.docker, se não existir
if [ ! -f .env ]; then
    cp .env.docker .env
    echo "✅ Arquivo .env criado a partir de .env.docker."
else
    echo "ℹ️ Arquivo .env já existe, não foi sobrescrito."
fi

# 2. Carrega variáveis de ambiente do arquivo .env
echo "🔐 Carregando variáveis de ambiente..."
export $(grep -v '^#' .env | xargs)

# 3. Subindo containers com Docker Compose
echo "✅ Subindo containers com Docker Compose..."
docker compose up -d --build

# 4. Aguardando o banco de dados ficar disponível
echo "✅ Aguardando o banco de dados ficar disponível..."
until docker compose exec web nc -z db 5432; do
  echo "⏳ Aguardando banco de dados ficar disponível..."
  sleep 2
done
echo "✅ Banco de dados está pronto!"

# 5. Aplicando migrações
echo "✅ Aplicando migrações..."
docker compose exec web python manage.py migrate

# 6. Coletando arquivos estáticos
echo "✅ Coletando arquivos estáticos..."
docker compose exec web python manage.py collectstatic --noinput

# 7. Criando superusuário (se necessário)
echo "✅ Criando superusuário (se necessário)..."
docker compose exec web python manage.py createsuperuser --noinput --username "${SUPERUSER_NAME}" --email "${SUPERUSER_EMAIL}" --password "${SUPERUSER_PASSWORD}" || true

# 8. Finalizando
echo "✅ Setup finalizado!"
echo "➡️ Acesse: http://localhost:8000"
echo "➡️ Admin: http://localhost:8000/admin"