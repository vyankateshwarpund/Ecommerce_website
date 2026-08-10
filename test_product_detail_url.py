import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client

print("==================================================================")
print("TESTING PRODUCT DETAIL URL RENDERING")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')
res = client.get('/products/apple-iphone-17-pro-max-cosmic-orange-256gb/')

print(f"Product Detail HTTP Status Code: {res.status_code}")
assert res.status_code == 200, f"Failed: Expected HTTP 200, got {res.status_code}"

print("==================================================================")
print("PRODUCT DETAIL PAGE RENDERS 100% CLEAN & WITHOUT ERRORS!")
print("==================================================================")
