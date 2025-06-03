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

print(f"🔍 Arquivo .env carregado: {env_file}")
# Carrega as variáveis do .env
config = Config(RepositoryEnv(str(env_file)))

# Segurança
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS').split(',')

# Superusuário automático
SUPERUSER_NAME = config('SUPERUSER_NAME')
SUPERUSER_EMAIL = config('SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = config('SUPERUSER_PASSWORD')

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
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1').split(',')

WSGI_APPLICATION = 'farmacia_escola.wsgi.application'

# Banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='farmaciaescola'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Segurança de sessão - padrões mínimos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 30 min
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

X_FRAME_OPTIONS = 'DENY'

# Segurança extra - padrões mínimos
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=False, cast=bool)
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=False, cast=bool)

# Redirecionamentos de login
LOGIN_URL = '/conta/login/'
LOGOUT_URL = '/conta/logout/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
