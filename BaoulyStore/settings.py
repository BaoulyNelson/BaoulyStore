from pathlib import Path
from decouple import AutoConfig, Csv

import dj_database_url
# Configuration des variables d'environnement
config = AutoConfig()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY (charge depuis le fichier .env)
SECRET_KEY = config('DJANGO_SECRET_KEY')

# DEBUG (charge depuis le fichier .env et convertit en booléen)
DEBUG = config('DJANGO_DEBUG', cast=bool)

# ALLOWED_HOSTS (charge depuis le fichier .env et sépare les valeurs par des virgules)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

ALLOWED_HOSTS = ['baoulystore.onrender.com', 'localhost', '127.0.0.1']


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # E-commerce related apps
    'store',
    # Additional packages
    'paypal.standard.ipn',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BaoulyStore.urls'

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

WSGI_APPLICATION = 'BaoulyStore.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),  # Charger depuis .env
        conn_max_age=600,
    )
}


# Password validation
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

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Login settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'liste_produits'
LOGOUT_REDIRECT_URL = '/'

# Django-crispy-forms configuration
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Django-allauth configuration
AUTHENTICATION_BACKENDS = (
    'store.authentication_backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

# MonCash settings
MONCASH_CLIENT_ID = config('MONCASH_CLIENT_ID')
MONCASH_SECRET_ID = config('MONCASH_SECRET_ID')
MONCASH_DEBUG = config('MONCASH_DEBUG', cast=bool)
