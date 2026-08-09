import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Product, Brand
from categories.models import Category

print("Updating Product Categories, Brands, and Product Images in Database...")

# Ensure Categories
cat_mobiles, _ = Category.objects.get_or_create(slug='mobiles', defaults={'name': 'Mobiles', 'icon': 'fas fa-mobile-screen-button'})
cat_electronics, _ = Category.objects.get_or_create(slug='electronics', defaults={'name': 'Electronics', 'icon': 'fas fa-laptop'})
cat_wearables, _ = Category.objects.get_or_create(slug='wearables', defaults={'name': 'Wearables', 'icon': 'fas fa-clock'})
cat_audio, _ = Category.objects.get_or_create(slug='audio', defaults={'name': 'Audio', 'icon': 'fas fa-headphones'})
cat_fashion, _ = Category.objects.get_or_create(slug='fashion', defaults={'name': 'Fashion', 'icon': 'fas fa-shirt'})
cat_home, _ = Category.objects.get_or_create(slug='home', defaults={'name': 'Home & Kitchen', 'icon': 'fas fa-house'})

# Ensure Brands
b_dell = Brand.objects.filter(name='Dell').first()
b_samsung = Brand.objects.filter(name='Samsung').first()
b_sony = Brand.objects.filter(name='Sony').first()
b_apple = Brand.objects.filter(name='Apple').first()
b_nike = Brand.objects.filter(name='Nike').first()
b_logitech = Brand.objects.filter(name='Logitech').first()

updates = [
    {
        'name': 'Pro Ultra Laptop (16GB RAM, 512GB SSD)',
        'category': cat_electronics,
        'brand': b_dell,
        'image': 'products/featured_laptop.jpg',
        'stock': 15,
        'price': 74999,
        'discount_price': 54999
    },
    {
        'name': 'Flagship Smartphone 5G (256GB Storage)',
        'category': cat_mobiles,
        'brand': b_samsung,
        'image': 'products/featured_smartphone.jpg',
        'stock': 22,
        'price': 69999,
        'discount_price': 49999
    },
    {
        'name': 'Wireless Noise-Canceling Headphones',
        'category': cat_audio,
        'brand': b_sony,
        'image': 'products/featured_headphones.jpg',
        'stock': 5,
        'price': 19999,
        'discount_price': 14999
    },
    {
        'name': 'Smartwatch Ultra 2 (AMOLED Display)',
        'category': cat_wearables,
        'brand': b_apple,
        'image': 'products/featured_smartwatch.jpg',
        'stock': 12,
        'price': 29999,
        'discount_price': 22999
    },
    {
        'name': 'Air-Cushioned Running Shoes',
        'category': cat_fashion,
        'brand': b_nike,
        'image': 'products/featured_shoes.jpg',
        'stock': 18,
        'price': 7999,
        'discount_price': 5499
    },
    {
        'name': 'Ergonomic Mesh Office Chair',
        'category': cat_home,
        'brand': b_logitech,
        'image': 'products/featured_chair.jpg',
        'stock': 8,
        'price': 14999,
        'discount_price': 10999
    }
]

for item in updates:
    p = Product.objects.filter(name=item['name']).first()
    if p:
        p.category = item['category']
        p.brand = item['brand']
        p.main_image = item['image']
        p.stock = item['stock']
        p.price = item['price']
        p.discount_price = item['discount_price']
        p.save()
        print(f"Updated {p.name}: Category={p.category.name}, Brand={p.brand.name if p.brand else 'None'}, Image={p.main_image.url}")

print("Database product images and categories fixed successfully!")
