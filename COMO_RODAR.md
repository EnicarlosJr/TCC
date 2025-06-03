# 📘 Guia de Instalação e Execução - Sistema Farmácia Escola UFVJM

Este documento fornece as instruções para instalar e executar o sistema web da Farmácia Escola da UFVJM em diferentes ambientes (desenvolvimento local ou com Docker).

---

## 📦 Requisitos

* Python 3.11+
* PostgreSQL 15+
* Git
* Docker e Docker Compose (opcional)

---

## 🧪 Ambiente de Desenvolvimento Local (sem Docker)

### 1. Clone o repositório

```bash
git clone https://github.com/EnicarlosJr/TCC.git
cd TCC
```

### 2. Crie o ambiente virtual

```bash
python -m venv env
source env/bin/activate       # Linux/macOS
.\env\Scripts\activate        # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz com base no `.env.example`:

```bash
cp .env.example .env
```

Edite as variáveis conforme seu ambiente local.

### 5. Execute o script de setup

```bash
./setup-dev.sh
```

Esse script irá:

* Verificar o PostgreSQL local
* Criar o banco `farmaciaescola` (se não existir)
* Aplicar migrações
* Criar superusuário (se necessário)
* Iniciar o servidor local em [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🐳 Ambiente com Docker (Desenvolvimento ou Produção)

### 1. Configure o arquivo `.env`

Crie um arquivo `.env` com base em `.env.example` e configure as variáveis conforme desejado (use `db` como DB\_HOST para Docker).

### 2. Suba os containers com Docker Compose

```bash
docker-compose up --build
```

Isso irá:

* Criar e inicializar o banco de dados PostgreSQL
* Construir a imagem do Django
* Executar o script `setup.sh` que faz migrações, cria superusuário e inicia o servidor Django

A aplicação estará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 🧾 Variáveis de Ambiente (`.env.example`)

Veja o conteúdo do arquivo `.env.example` no repositório para saber quais variáveis precisam ser configuradas:

* Dados do banco (DB\_NAME, DB\_USER, DB\_PASSWORD, etc)
* Configurações do Django (DEBUG, SECRET\_KEY, ALLOWED\_HOSTS)
* Superusuário padrão (nome, email e senha)

---

## 🛡️ Considerações para Produção

* Defina `DEBUG=False`
* Configure corretamente `ALLOWED_HOSTS`
* Habilite HTTPS e cookies seguros:

  ```env
  SESSION_COOKIE_SECURE=True
  CSRF_COOKIE_SECURE=True
  SECURE_SSL_REDIRECT=True
  SECURE_HSTS_SECONDS=31536000
  SECURE_HSTS_INCLUDE_SUBDOMAINS=True
  SECURE_HSTS_PRELOAD=True
  SECURE_CONTENT_TYPE_NOSNIFF=True
  SECURE_BROWSER_XSS_FILTER=True
  ```

---

## 🧪 Testes Automatizados

> *Em desenvolvimento*
> Futuramente serão utilizados:

* **pytest**
* **Django TestCase**

---

## 👤 Autor

**Enicarlos Pereira Gonçalves Júnior**
Aluno de Sistemas de Informação - UFVJM
GitHub: [@EnicarlosJr](https://github.com/EnicarlosJr)
