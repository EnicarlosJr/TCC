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
echo "⏳ Aguardando o banco de dados ficar disponível..."
until docker compose exec web nc -zv db 5432; do
  echo "⏳ Aguardando banco de dados ficar disponível..."
  sleep 2
done
echo "✅ Banco de dados está pronto!"

# 5. Verificando e criando migrações por app
apps=("paciente" "consulta" "listagem_pacientes" "tela_inicial" "relatorios" "login" "core")

echo "📦 Verificando migrações por app..."
for app in "${apps[@]}"; do
  echo "🔍 Verificando app: $app"
  docker compose exec web sh -c "
    if [ ! -d $app/migrations ] || [ \$(ls $app/migrations | grep -c '^[0-9].*\.py$') -eq 0 ]; then
      echo '📁 Criando migrações para $app...'
      python manage.py makemigrations $app
    else
      echo '✔️ Migrações já existentes para $app.'
    fi
  "
done

# 6. Aplicando migrações por app
echo "✅ Aplicando migrações por app..."
for app in "${apps[@]}"; do
  echo "📥 Migrando app: $app..."
  docker compose exec web python manage.py migrate $app --noinput
done

# 7. Coletando arquivos estáticos
echo "✅ Coletando arquivos estáticos..."
docker compose exec web python manage.py collectstatic --noinput

# 8. Criando superusuário (se necessário)
echo "✅ Criando superusuário (se necessário)..."
docker compose exec web python manage.py createsuperuser --noinput --username "${SUPERUSER_NAME}" --email "${SUPERUSER_EMAIL}" || true

# 9. Finalizando
echo "✅ Setup finalizado!"
echo "➡️ Acesse: http://localhost:8000"
echo "➡️ Admin: http://localhost:8000/admin"
