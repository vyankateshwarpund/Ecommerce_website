import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client, override_settings
from django.core import mail
from accounts.models import User

client = Client(HTTP_HOST='127.0.0.1:8000')

print("==================================================================")
print("GENERATING PASSWORD RESET LINK FOR DEMO USER")
print("==================================================================")

with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    client.post('/password-reset/', {'email': 'pundsaurav@gmail.com'})
    if mail.outbox:
        body = mail.outbox[0].body
        link = re.search(r'http://127\.0\.0\.1:8000([^\s]+)', body).group(0)
        print("Generated Password Reset Link:")
        print(link)

print("==================================================================")
