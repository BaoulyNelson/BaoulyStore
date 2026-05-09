"""
Base settings for BaoulyStore.
Shared across all environments (development, production).
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# Project root: two levels up from this file (config/settings/base.py → root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / '.env')

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',
]

LOCAL_APPS = [
    'apps.catalogue',
    'apps.cart',
    'apps.reviews',
    'apps.accounts',
    'apps.pages',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BaoulyStore.urls'
WSGI_APPLICATION = 'BaoulyStore.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
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
                'apps.cart.context_processors.cart_context',
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Database (overridden per environment)
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'store'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'apps.accounts.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'catalogue:index'
LOGOUT_REDIRECT_URL = 'catalogue:index'

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'America/Port-au-Prince'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & Media files
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------------------------
# Crispy forms
# ---------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ---------------------------------------------------------------------------
# Email (base — SMTP Gmail; override in dev to use console backend)
# ---------------------------------------------------------------------------
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', EMAIL_HOST_USER)

# ---------------------------------------------------------------------------
# MonCash payment gateway
# ---------------------------------------------------------------------------
MONCASH_CLIENT_ID = os.getenv('MONCASH_CLIENT_ID')
MONCASH_SECRET_ID = os.getenv('MONCASH_SECRET_ID')
MONCASH_DEBUG = os.getenv('MONCASH_DEBUG', 'True') == 'True'

# ---------------------------------------------------------------------------
# Admin site customisation
# ---------------------------------------------------------------------------
ADMIN_SITE_HEADER = "BaoulyStore Administration"
ADMIN_SITE_TITLE = "BaoulyStore Admin"
ADMIN_INDEX_TITLE = "Tableau de bord"


from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG:   'debug',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR:   'danger',  # ⚠️ Bootstrap utilise 'danger' pas 'error'
}