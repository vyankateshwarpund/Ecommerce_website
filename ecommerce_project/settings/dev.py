"""ShopSphere — Development Settings"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Auto-detect real SMTP credentials vs Console fallback
if env('EMAIL_HOST_USER', default='').endswith('@domain.com') or not env('EMAIL_HOST_USER', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
