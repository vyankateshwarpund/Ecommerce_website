import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from categories.models import Category

cats_preference = [
    ('Mobiles', 'mobiles', 'fas fa-mobile-screen-button', 'Smartphones & 5G Devices', 1),
    ('Electronics', 'electronics', 'fas fa-laptop', 'Laptops & Computers', 2),
    ('Wearables', 'wearables', 'fas fa-clock', 'Smartwatches & Fitness Bands', 3),
    ('Audio', 'audio', 'fas fa-headphones', 'Headphones & Speakers', 4),
    ('Gaming', 'gaming', 'fas fa-gamepad', 'Consoles & Gaming Gear', 5),
    ('Fashion', 'fashion', 'fas fa-shirt', 'Clothing & Footwear', 6),
    ('Beauty', 'beauty', 'fas fa-wand-magic-sparkles', 'Skincare & Cosmetics', 7),
    ('Home & Kitchen', 'home', 'fas fa-house', 'Furniture & Appliances', 8),
    ('Automotive', 'automotive', 'fas fa-car', 'Auto Gear & Accessories', 9),
    ('Books', 'books', 'fas fa-book-open', 'Fiction & Educational Books', 10),
    ('Toys & Baby', 'toys', 'fas fa-puzzle-piece', 'Baby Toys & Essentials', 11),
    ('Sports & Fitness', 'sports', 'fas fa-dumbbell', 'Gym & Athletic Equipment', 12),
    ('Pet Supplies', 'pets', 'fas fa-paw', 'Pet Food & Toys', 13),
    ('Bags & Luggage', 'bags', 'fas fa-suitcase', 'Travel Bags & Backpacks', 14),
    ('Accessories', 'accessories', 'fas fa-plug', 'Tech & Mobile Accessories', 15),
]

for name, slug, icon, desc, order in cats_preference:
    c, created = Category.objects.update_or_create(
        slug=slug,
        defaults={
            'name': name,
            'icon': icon,
            'description': desc,
            'order': order,
            'is_active': True,
            'is_featured': True
        }
    )
    print(f"Category Order {c.order}: {c.name} ({c.slug}) -> {c.icon}")

print("\nAll 15 Categories successfully seeded in database in exact preference order!")
