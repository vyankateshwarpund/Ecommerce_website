"""ShopSphere — Development Settings"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use console email in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show all SQL queries in terminal (optional — set to True for debugging)
# LOGGING = {
#     'version': 1,
#     'handlers': {'console': {'class': 'logging.StreamHandler'}},
#     'loggers': {'django.db.backends': {'handlers': ['console'], 'level': 'DEBUG'}},
# }
