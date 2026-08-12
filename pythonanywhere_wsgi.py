# ============================================================
# PythonAnywhere WSGI Configuration File
# Place this code inside your PythonAnywhere WSGI configuration file:
# /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
# ============================================================

import os
import sys

# 1. Add your project directory to sys.path
# Replace 'YOUR_USERNAME' with your actual PythonAnywhere username
path = '/home/YOUR_USERNAME/ECommers_Project'
if path not in sys.path:
    sys.path.append(path)

# 2. Set Django Settings Module to Production Settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_project.settings.prod'

# 3. Load WSGI Application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
