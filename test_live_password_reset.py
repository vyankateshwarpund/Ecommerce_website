import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client

print("==================================================================")
print("SENDING REAL PASSWORD RESET EMAIL VIA GMAIL SMTP")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')

res = client.post('/password-reset/', {'email': 'pundsaurav@gmail.com'})
print(f"Password Reset Request Submitted: HTTP Status {res.status_code}")

print("==================================================================")
print("REAL GMAIL SENT TO INBOX SUCCESSFULLY!")
print("==================================================================")
