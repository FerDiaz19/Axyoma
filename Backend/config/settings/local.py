from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database PostgreSQL con configuracion UTF-8 corregida
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'axyoma',
        'USER': 'postgres',
        'PASSWORD': '123456789',  # Cambia esto por tu contraseña real
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    }
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

