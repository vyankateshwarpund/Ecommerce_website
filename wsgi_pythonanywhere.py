"""
SPCart — PythonAnywhere WSGI Configuration
Place this file path in your PythonAnywhere Web Tab > WSGI configuration file field,
OR copy this content into the WSGI file shown in your Web Tab.
"""

import os
import sys

# ── 1. Add project to Python path ──────────────────────────────────────────────
# Replace YOUR_USERNAME with your PythonAnywhere username
path = '/home/YOUR_USERNAME/ECommers_Project'
if path not in sys.path:
    sys.path.insert(0, path)

# ── 2. Point to Django settings ────────────────────────────────────────────────
os.environ['DJANGO_SETTINGS_MODULE'] = 'ecommerce_project.settings.dev'

# ── 3. Load WSGI application ───────────────────────────────────────────────────
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
