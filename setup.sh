#!/bin/bash

echo "✅ Iniciando setup automático do Sistema Farmácia Escola..."

if [ ! -f .env ]; then
    cp .env.docker .env
    echo "✅ Arquivo .env criado a partir de .env.docker."
else
    echo "ℹ️ Arquivo .env já existe, não foi sobrescrito."
fi

echo "✅ Subindo containers com Docker Compose..."
docker compose up -d --build

echo "✅ Aguardando o banco de dados ficar disponível..."
until docker compose exec web nc -z db 5432; do
  echo "⏳ Aguardando banco de dados ficar disponível..."
  sleep 2
done
echo "✅ Banco de dados está pronto!"

echo "✅ Aplicando migrações..."
docker compose exec web python manage.py migrate

echo "✅ Coletando arquivos estáticos..."
docker compose exec web python manage.py collectstatic --noinput

echo "✅ Criando superusuário (se necessário)..."
docker compose exec web python manage.py createsuperuser --noinput || true

echo "✅ Setup finalizado!"
echo "➡️ Acesse: http://localhost:8000"
echo "➡️ Admin: http://localhost:8000/admin"
