import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from categories.models import Category
from products.models import Brand, Product
from django.core.files import File

def seed_database():
    print("Seeding All 12 E-Commerce Categories...")
    cats_data = [
        {'name': 'Mobiles', 'slug': 'mobiles', 'icon': 'fas fa-mobile-screen-button', 'description': 'Smartphones, 5G devices & mobile accessories', 'is_featured': True},
        {'name': 'Electronics', 'slug': 'electronics', 'icon': 'fas fa-laptop', 'description': 'Laptops, audio, monitors & computer accessories', 'is_featured': True},
        {'name': 'Fashion', 'slug': 'fashion', 'icon': 'fas fa-shirt', 'description': 'Men & women apparel, footwear & watches', 'is_featured': True},
        {'name': 'Gaming', 'slug': 'gaming', 'icon': 'fas fa-gamepad', 'description': 'Consoles, gaming laptops & accessories', 'is_featured': True},
        {'name': 'Home & Living', 'slug': 'home', 'icon': 'fas fa-house', 'description': 'Furniture, home decor & kitchen appliances', 'is_featured': True},
        {'name': 'Beauty', 'slug': 'beauty', 'icon': 'fas fa-wand-magic-sparkles', 'description': 'Skincare, haircare, makeup & grooming', 'is_featured': True},
        {'name': 'Books', 'slug': 'books', 'icon': 'fas fa-book-open', 'description': 'Fiction, non-fiction, academic & educational books', 'is_featured': False},
        {'name': 'Sports & Fitness', 'slug': 'sports', 'icon': 'fas fa-dumbbell', 'description': 'Gym equipment, sportswear & outdoor gear', 'is_featured': False},
        {'name': 'Automotive', 'slug': 'automotive', 'icon': 'fas fa-car', 'description': 'Car accessories, riding gear & auto care', 'is_featured': False},
        {'name': 'Toys & Baby', 'slug': 'toys', 'icon': 'fas fa-puzzle-piece', 'description': 'Baby essentials, learning toys & games', 'is_featured': False},
        {'name': 'Office Supplies', 'slug': 'office', 'icon': 'fas fa-briefcase', 'description': 'Stationery, desk organization & paper', 'is_featured': False},
        {'name': 'Pet Supplies', 'slug': 'pets', 'icon': 'fas fa-paw', 'description': 'Dog food, cat toys & pet grooming', 'is_featured': False},
    ]

    categories = {}
    for c_info in cats_data:
        cat, created = Category.objects.update_or_create(
            name=c_info['name'],
            defaults={
                'slug': c_info['slug'],
                'icon': c_info['icon'],
                'description': c_info['description'],
                'is_featured': c_info['is_featured'],
                'is_active': True
            }
        )
        categories[cat.slug] = cat
        print(f"Category set: {cat.name} ({cat.slug})")

    print("Seeding Top Brands...")
    brands_data = ['Apple', 'Samsung', 'Sony', 'Nike', 'Adidas', 'LG', 'Microsoft', 'Google']
    brands = {}
    for b_name in brands_data:
        b, _ = Brand.objects.get_or_create(name=b_name, defaults={'is_featured': True})
        brands[b_name] = b

    print("Seeding Real Products with Genuine Stock...")
    products_data = [
        {
            'name': 'Pro Ultra Laptop (16GB RAM, 512GB SSD)',
            'slug': 'pro-ultra-laptop-16gb',
            'category': categories['electronics'],
            'brand': brands['Apple'],
            'description': 'Ultra-thin high performance laptop with M2 chip, 16GB unified memory, and 512GB SSD storage. Retina display with True Tone technology.',
            'short_description': 'Ultra-thin high performance laptop with 16GB RAM & 512GB SSD.',
            'price': 99999.00,
            'discount_price': 79999.00,
            'stock': 15,
            'badge': 'bestseller',
            'rating': 4.8,
            'reviews_count': 256,
            'is_featured': True,
            'is_deal': False,
            'image_path': 'static/images/featured_laptop.jpg'
        },
        {
            'name': 'Flagship Smartphone 5G (256GB Storage)',
            'slug': 'flagship-smartphone-5g',
            'category': categories['mobiles'],
            'brand': brands['Samsung'],
            'description': 'Pro-grade camera with 108MP main sensor, 120Hz AMOLED display, 5000mAh battery, and superfast 5G connectivity.',
            'short_description': 'Pro-grade camera 5G smartphone with 120Hz display.',
            'price': 76999.00,
            'discount_price': 64999.00,
            'stock': 22,
            'badge': 'new',
            'rating': 5.0,
            'reviews_count': 412,
            'is_featured': True,
            'is_deal': True,
            'image_path': 'static/images/featured_smartphone.jpg'
        },
        {
            'name': 'Wireless Noise-Canceling Headphones',
            'slug': 'wireless-noise-canceling-headphones',
            'category': categories['electronics'],
            'brand': brands['Sony'],
            'description': 'Industry leading active noise cancellation with dual noise sensor technology. Up to 30 hours battery life with quick charging.',
            'short_description': 'Active noise canceling wireless headphones with 30h battery.',
            'price': 14299.00,
            'discount_price': 9999.00,
            'stock': 5,
            'badge': 'trending',
            'rating': 4.2,
            'reviews_count': 188,
            'is_featured': True,
            'is_deal': True,
            'image_path': 'static/images/featured_headphones.jpg'
        },
        {
            'name': 'Smartwatch Ultra 2 (AMOLED Display)',
            'slug': 'smartwatch-ultra-2',
            'category': categories['electronics'],
            'brand': brands['Apple'],
            'description': 'Rugged titanium case, precision dual-frequency GPS, heart rate monitor, ECG app, and up to 36 hours of battery life.',
            'short_description': 'Rugged titanium smartwatch with heart rate & GPS.',
            'price': 19999.00,
            'discount_price': 11999.00,
            'stock': 12,
            'badge': 'limited',
            'rating': 4.7,
            'reviews_count': 320,
            'is_featured': True,
            'is_deal': True,
            'image_path': 'static/images/featured_smartwatch.jpg'
        },
        {
            'name': 'Air-Cushioned Running Shoes',
            'slug': 'air-cushioned-running-shoes',
            'category': categories['fashion'],
            'brand': brands['Nike'],
            'description': 'Breathable mesh running shoes with impact-absorbing air cushion soles for maximum comfort during long workouts.',
            'short_description': 'Breathable mesh running shoes with air cushion sole.',
            'price': 7999.00,
            'discount_price': 4999.00,
            'stock': 18,
            'badge': 'bestseller',
            'rating': 4.6,
            'reviews_count': 145,
            'is_featured': True,
            'is_deal': False,
            'image_path': 'static/images/featured_headphones.jpg'
        },
        {
            'name': 'Ergonomic Mesh Office Chair',
            'slug': 'ergonomic-mesh-office-chair',
            'category': categories['home'],
            'brand': brands['LG'],
            'description': 'High-back ergonomic chair with adjustable lumbar support, 3D armrests, and breathable mesh backrest for all-day comfort.',
            'short_description': 'High-back ergonomic chair with lumbar support.',
            'price': 16999.00,
            'discount_price': 12499.00,
            'stock': 8,
            'badge': 'trending',
            'rating': 4.5,
            'reviews_count': 92,
            'is_featured': True,
            'is_deal': False,
            'image_path': 'static/images/featured_laptop.jpg'
        }
    ]

    for p_info in products_data:
        image_path = p_info.pop('image_path')
        p, created = Product.objects.update_or_create(
            name=p_info['name'],
            defaults=p_info
        )
        if os.path.exists(image_path) and not p.main_image:
            with open(image_path, 'rb') as f:
                p.main_image.save(os.path.basename(image_path), File(f), save=True)
        print(f"Product updated: {p.name} (Stock: {p.stock})")

    print("\nAll 12 Categories, Brands & Products successfully seeded into DB!")

if __name__ == '__main__':
    seed_database()
