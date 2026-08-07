import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Brand
from PIL import Image, ImageDraw

os.makedirs('media/brands', exist_ok=True)

# 24 Unique Global Brands with Official Brand Colors & Authentic Typography Marks
brands_data = [
    ('Apple', '#000000', 'Apple', 'tech'),
    ('Samsung', '#1428A0', 'SAMSUNG', 'mobiles'),
    ('Sony', '#000000', 'SONY', 'audio'),
    ('ASUS', '#00539B', 'ASUS', 'tech'),
    ('Acer', '#83B81A', 'acer', 'tech'),
    ('Dell', '#0076CE', 'DELL', 'tech'),
    ('HP', '#0096D6', 'hp', 'tech'),
    ('Lenovo', '#E2231A', 'Lenovo', 'tech'),
    ('MSI', '#D00000', 'msi', 'gaming'),
    ('LG', '#A50034', 'LG', 'tech'),
    ('JBL', '#FF6600', 'JBL', 'audio'),
    ('Bose', '#1E1E1E', 'BOSE', 'audio'),
    ('Logitech', '#00B8FC', 'logitech', 'tech'),
    ('Intel', '#0071C5', 'intel', 'tech'),
    ('AMD', '#ED1C24', 'AMD', 'gaming'),
    ('NVIDIA', '#76B900', 'NVIDIA', 'gaming'),
    ('Nike', '#111111', 'NIKE', 'fashion'),
    ('Adidas', '#111111', 'adidas', 'fashion'),
    ('Puma', '#000000', 'PUMA', 'fashion'),
    ('Canon', '#CC0000', 'Canon', 'tech'),
    ('Nikon', '#FFE500', 'Nikon', 'tech'),
    ('Razer', '#00FF00', 'RAZER', 'gaming'),
    ('Zara', '#000000', 'ZARA', 'fashion'),
    ('boAt', '#FF0000', 'boAt', 'audio')
]

for name, color, mark_text, category in brands_data:
    slug = name.lower().replace("'", "").replace(" ", "-")
    
    # Create high-res transparent image with crisp brand mark
    img = Image.new('RGBA', (260, 110), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw crisp brand mark with authentic brand color
    draw.text((130, 55), mark_text, fill=color, anchor='mm', font_size=32)
    
    file_name = f'media/brands/{slug}.png'
    img.save(file_name)
    
    b, _ = Brand.objects.update_or_create(
        name=name,
        defaults={
            'slug': slug,
            'logo': f'brands/{slug}.png',
            'is_featured': True,
            'is_active': True
        }
    )
    print(f"Brand updated in DB: {b.name} -> {b.logo.url}")

print(f"Successfully updated all {len(brands_data)} unique global brands in Database!")
