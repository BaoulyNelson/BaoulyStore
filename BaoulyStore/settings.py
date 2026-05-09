"""Development settings — never use in production."""
from settings.base import *

DEBUG = True

# Use console email backend in development — no actual emails sent
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Relax password validation for dev convenience
AUTH_PASSWORD_VALIDATORS = []

# Django Debug Toolbar (optional — install if needed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
# INTERNAL_IPS = ['127.0.0.1']
