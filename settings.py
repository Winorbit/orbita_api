import os
import psycopg2
import logging.config

from django.conf.global_settings import AUTHENTICATION_BACKENDS
from pythonjsonlogger import jsonlogger
import yaml
from dotenv import load_dotenv

def load_envfile(envfile: str = ".env"):
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    dotenv_path_alter = os.path.join(os.path.dirname(__file__), ".envfile")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

        return os.environ
    else:
        if os.path.exists(dotenv_path_alter):
            load_dotenv(dotenv_path_alter)
            return os.environ
        else:
            raise Exception("Envfile doesn't exist")

load_envfile()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY")
HOST = os.environ.get("HOST")
NGINX_PROXY_PORT = os.environ.get("NGINX_PROXY_PORT") 

if os.environ.get("ENV_TYPE") != "prod":
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ['31.131.28.206', 'web-api', "web-ui", "winorbita.com"]

DEBUG = os.environ.get("DEBUG")

with open('logger_config.yml', 'r') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)

logger = logging.getLogger('api_logger')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'api',
    'rest_framework',
    'tinymce',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = False

PORT_UI = os.environ.get("PORT_UI")

CORS_ORIGIN_WHITELIST = [
    f'http://localhost:{PORT_UI}',
    f'http://localhost:{NGINX_PROXY_PORT}',
    f'http://0.0.0.0:{PORT_UI}',
    f'http://{HOST}:{NGINX_PROXY_PORT}',
    f'http://{HOST}:{PORT_UI}',
    f'http://ui:{PORT_UI}',
    'http://winorbita.com',
    f'http://winorbita.com:{PORT_UI}',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASS"),
        'HOST': os.environ.get("HOST"),
        'PORT': os.environ.get("DB_PORT"),
        'TEST': {
            'NAME': 'postgres_for_tests',
        },
    },
}


WSGI_APPLICATION = 'wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'deploy_static')

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ),
    'PAGE_SIZE': 10
}

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'winterorbita@gmail.com'
EMAIL_HOST_PASSWORD = 'winterorbita2020'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
