from logging import config
import os
from pathlib import Path
from decouple import Config, RepositoryEnv

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Sobe até /TCC/

# Define qual ambiente usar: dev (padrão) ou production
ENV = os.getenv('DJANGO_ENV', 'dev')

# Caminho para o .env adequado
env_file = BASE_DIR / f'.env.{ENV}'
print("🔍 Arquivo .env carregado:", env_file)

# Verifica se o arquivo existe
if not env_file.exists():
    raise FileNotFoundError(f"Arquivo de configuração {env_file} não encontrado.")

# Carrega as variáveis do .env
config = Config(RepositoryEnv(str(env_file)))

# Segurança
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1').split(',')

# Superusuário automático
SUPERUSER_NAME = config('SUPERUSER_NAME', default='admin')
SUPERUSER_EMAIL = config('SUPERUSER_EMAIL', default='admin@admin.com')
SUPERUSER_PASSWORD = config('SUPERUSER_PASSWORD', default='admin')

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps do projeto
    'paciente',
    'listagem_pacientes',
    'consulta',
    'tela_inicial',
    'relatorios',
    'django_extensions',
    'login',
    'widget_tweaks',
    'core',
    'django_cas_ng',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'farmacia_escola.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'farmacia_escola.wsgi.application'

# Banco de dados (PostgreSQL ou SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='farmaciaescola'),
        'USER': config('DB_USER', default='juliana'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='db'),  # Para Docker, será 'db'
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Autenticação
AUTH_USER_MODEL = 'login.CustomUser'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 30 min
X_FRAME_OPTIONS = 'DENY'

# Redirecionamentos de login
LOGIN_URL = '/conta/login/'
LOGOUT_URL = '/conta/logout/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Segurança extra para ambientes de produção
if ENV == 'prod':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 3600  # 1 hora
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Desabilitado para ambiente de desenvolvimento
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'INFO'},
}
