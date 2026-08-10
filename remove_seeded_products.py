import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Product, ProductImage

print("==================================================================")
print("REMOVING ALL 160 SEEDED PRODUCTS FROM DATABASE")
print("==================================================================")

# Delete products with ID >= 8
seeded_products = Product.objects.filter(id__gte=8)
count = seeded_products.count()

# Delete associated images
ProductImage.objects.filter(product__in=seeded_products).delete()

# Delete product records
deleted_info = seeded_products.delete()

print(f"[OK] Successfully deleted {count} seeded products!")
print(f"Remaining Products in Database: {Product.objects.count()}")

remaining = Product.objects.all()
for p in remaining:
    print(f"  • ID {p.id}: {p.name} ({p.category.name if p.category else 'No Category'})")

print("==================================================================")
print("DATABASE CLEANED & RESTORED TO PREVIOUS STATE SUCCESSFULLY!")
print("==================================================================")
