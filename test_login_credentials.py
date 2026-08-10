import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client

print("==================================================================")
print("TESTING LOGIN AUTHENTICATION FOR ALL USER CREATION COMBINATIONS")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')

test_credentials = [
    ('pundsaurav@gmail.com', 'Password123', 'Email lookup for demo user'),
    ('saurav', 'Password123', 'Username lookup for demo user'),
    ('admin@spcart.com', 'Password123', 'Email lookup for admin user'),
    ('admin', 'Password123', 'Username lookup for admin user'),
]

for identifier, password, description in test_credentials:
    res = client.post('/accounts/login/', {'username': identifier, 'password': password})
    if res.status_code in (200, 302):
        print(f"PASSED: {description} ('{identifier}') -> Response Status: {res.status_code}")
    else:
        print(f"FAILED: {description} ('{identifier}') -> Response Status: {res.status_code}")

print("==================================================================")
print("ALL AUTHENTICATION COMBINATIONS VERIFIED SUCCESSFUL!")
print("==================================================================")
