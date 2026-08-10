import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Product

print("==================================================================")
print("INSPECTING CURRENT PRODUCTS IN DATABASE")
print("==================================================================")

products = Product.objects.all().order_by('id')
print(f"Total Products in DB: {products.count()}")
for p in products[:15]:
    print(f"ID: {p.id} | Name: {p.name} | Category: {p.category.name if p.category else None}")

print("==================================================================")
