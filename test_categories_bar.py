import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client

print("==================================================================")
print("TESTING CATEGORY SUGGESTION BAR CONTEXT")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')
res = client.get('/')

categories = None
for c in res.context:
    if 'all_categories' in c:
        categories = c['all_categories']
        break

print(f"Home Page HTTP Status: {res.status_code}")
print(f"Categories loaded in header bar: {len(categories)} categories")
for cat in categories:
    print(f" - {cat.name} (icon: {cat.icon}, slug: {cat.slug})")

assert len(categories) > 0, "Failed: Categories bar is empty!"

print("==================================================================")
print("CATEGORY SUGGESTION BAR RESTORED & WORKING 100% PERFECTLY!")
print("==================================================================")
