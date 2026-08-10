import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client, override_settings
from django.core import mail

c = Client(HTTP_HOST='127.0.0.1:8000')

with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    c.post('/password-reset/', {'email': 'pundsaurav@gmail.com'})
    email_body = mail.outbox[0].body
    print("Email body:")
    print(email_body)
    link = re.search(r'http://127\.0\.0\.1:8000([^\s]+)', email_body).group(1)
    print("Found link:", link)
    res = c.get(link)
    print("GET Status:", res.status_code)
    print("Location header:", res.headers.get('Location'))
