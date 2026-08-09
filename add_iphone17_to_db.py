import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Product, Brand, ProductImage
from categories.models import Category

# Source generated image
src_image = r"C:\Users\NS\.gemini\antigravity\brain\c4a281be-c050-413d-b102-f7c4f2908e52\iphone17_pro_max_1786276513686.jpg"
target_dir = "media/products"
os.makedirs(target_dir, exist_ok=True)
target_image = os.path.join(target_dir, "iphone17_pro_max.jpg")

if os.path.exists(src_image):
    shutil.copy(src_image, target_image)
    print("Copied generated iPhone 17 Pro Max image to media/products/iphone17_pro_max.jpg")

# Ensure Category & Brand
cat_mobiles, _ = Category.objects.get_or_create(
    slug='mobiles',
    defaults={'name': 'Mobiles', 'icon': 'fas fa-mobile-screen-button', 'order': 1, 'is_active': True}
)

brand_apple, _ = Brand.objects.get_or_create(
    name='Apple',
    defaults={'slug': 'apple', 'is_active': True, 'is_featured': True}
)

# Create Product
product, created = Product.objects.update_or_create(
    slug='apple-iphone-17-pro-max-cosmic-orange-256gb',
    defaults={
        'name': 'Apple iPhone 17 Pro Max (Cosmic Orange, 256 GB)',
        'category': cat_mobiles,
        'brand': brand_apple,
        'price': 144900.00,
        'discount_price': 134900.00,
        'stock': 15,
        'is_available': True,
        'is_featured': True,
        'is_deal': True,
        'badge': 'bestseller',
        'rating': 4.9,
        'reviews_count': 1280,
        'main_image': 'products/iphone17_pro_max.jpg',
        'description': 'Experience the pinnacle of smartphone innovation with the Apple iPhone 17 Pro Max in Cosmic Orange (256 GB). Powered by the groundbreaking A19 Pro Bionic chip, featuring a Super Retina XDR OLED display with 120Hz ProMotion, Aerospace-grade Titanium chassis, ceramic shield front, and an advanced 48MP Fusion Triple Camera system with 10x Optical Zoom.',
        'short_description': 'A19 Pro Chip, 6.9-inch Super Retina XDR, 48MP Triple Camera, Titanium Design, Cosmic Orange'
    }
)

print(f"Product {'Created' if created else 'Updated'}: {product.name} (ID: {product.id})")
print(f"URL Slug: {product.slug}")
