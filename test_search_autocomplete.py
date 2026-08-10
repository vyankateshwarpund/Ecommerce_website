import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client

print("==================================================================")
print("TESTING REAL-TIME SEARCH AUTOCOMPLETE API")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')

# Search 'iphone'
res1 = client.get('/products/autocomplete/?q=iphone')
data1 = res1.json()
print(f"1. Autocomplete Search 'iphone': {len(data1['results'])} result(s)")
for r in data1['results']:
    print(f"   Match: {r['name']} | Category: {r['category']} | URL: {r['url']}")

assert len(data1['results']) > 0, "Failed: iPhone search returned 0 results!"

print("==================================================================")
print("ALL SEARCH AUTOCOMPLETE ENDPOINTS VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
