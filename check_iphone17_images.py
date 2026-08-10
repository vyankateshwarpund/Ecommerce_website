import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.conf import settings
from products.models import Product, ProductImage

print("==================================================================")
print("CHECKING IPHONE 17 PRO MAX IMAGES & GALLERY")
print("==================================================================")

iphone = Product.objects.filter(slug__icontains='iphone-17').first()
if iphone:
    print(f"Product Found: ID {iphone.id} | Name: {iphone.name}")
    print(f"Main Image: {iphone.main_image}")
    
    # Check media folder for files
    media_dir = settings.MEDIA_ROOT
    all_files = []
    for root, dirs, files in os.walk(media_dir):
        for f in files:
            all_files.append(os.path.join(root, f))
    
    print(f"Total media files found: {len(all_files)}")
    iphone_files = [f for f in all_files if 'iphone' in f.lower() or '17' in f.lower()]
    for f in iphone_files:
        print(f"  • {os.path.relpath(f, media_dir)}")

print("==================================================================")
