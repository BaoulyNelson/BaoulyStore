from pathlib import Path
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
SILENCED_SYSTEM_CHECKS = ["models.W036"]

# Chemin de base
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default_secret_key')

# Mode debug
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hôtes autorisés
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application installée
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'paypal.standard.ipn',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# Middleware
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

# URL configuration
ROOT_URLCONF = 'BaoulyStore.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'store/templates'],
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

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'default_db_name'),
        'USER': os.getenv('DB_USER', 'default_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
    }
}

# Configuration de l'email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

MONCASH_CLIENT_ID = os.getenv('MONCASH_CLIENT_ID', '')
MONCASH_SECRET_ID = os.getenv('MONCASH_SECRET_ID', '')
MONCASH_DEBUG = os.getenv('MONCASH_DEBUG', 'False') == 'True'

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOGIN_URL = '/connexion/'  # URL de la page de connexion
LOGOUT_REDIRECT_URL = 'index'
# URL pour accéder aux fichiers statiques
STATIC_URL = '/static/'

# Chemin où Django recherche les fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / "static",  # si vos fichiers statiques sont dans un dossier "static" à la racine de votre projet
]

# Ce répertoire est utilisé pour collecter tous les fichiers statiques lors de la mise en production
STATIC_ROOT = BASE_DIR / "staticfiles"  # utile lorsque vous utilisez 'collectstatic'
# URL où les fichiers médias seront accessibles
MEDIA_URL = '/media/'

# Configuration Django-allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Utilisation du backend par défaut
)

SITE_ID = 1
