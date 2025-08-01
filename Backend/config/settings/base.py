
# ---------------------------------------------------------------------------- #

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------- #

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tx1+zb7vwker=f)q05g#=9((d!^j#^x%4q_v!cw66_n5(_0-pn'

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ---------------------------------------------------------------------------- #

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',  # Requerido para TokenAuthentication
    'drf_yasg',  # Swagger documentation
]

LOCAL_APPS = [
    'apps.users',
    'apps.subscriptions',
    'apps.evaluaciones',
    'apps.admin_bd',

    'anorlondo', # Evaluaciones (empleados).
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------- #

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_PROJECT_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------- #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'axyomadb',
        'USER': 'postgres',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ---------------------------------------------------------------------------- #

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

# ---------------------------------------------------------------------------- #

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configuración de codificación UTF-8
import locale
import os
os.environ.setdefault('LANG', 'es_MX.UTF-8')
os.environ.setdefault('LC_ALL', 'es_MX.UTF-8')

# ---------------------------------------------------------------------------- #

STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_PROJECT_DIR / 'statics' ]

# ---------------------------------------------------------------------------- #

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import sys
import locale

# Configurar la codificacion por defecto
if sys.platform.startswith('win'):
    locale.setlocale(locale.LC_ALL, 'Spanish_Spain.utf8')
else:
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# ---------------------------------------------------------------------------- #

# Configuracion para REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'UNICODE_JSON': True,
}

# ---------------------------------------------------------------------------- #

# Configuracion de CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# ---------------------------------------------------------------------------- #

# Configuracion adicional para CORS
CORS_PREFLIGHT_MAX_AGE = 86400

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ---------------------------------------------------------------------------- #
