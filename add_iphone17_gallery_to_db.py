import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Product, ProductImage

product = Product.objects.filter(slug='apple-iphone-17-pro-max-cosmic-orange-256gb').first()
if not product:
    print("iPhone 17 Pro Max product not found!")
    exit()

target_dir = "media/products/gallery"
os.makedirs(target_dir, exist_ok=True)

gallery_sources = [
    (r"C:\Users\NS\.gemini\antigravity\brain\c4a281be-c050-413d-b102-f7c4f2908e52\iphone17_front_1786276754801.jpg", "iphone17_front.jpg", "Front View"),
    (r"C:\Users\NS\.gemini\antigravity\brain\c4a281be-c050-413d-b102-f7c4f2908e52\iphone17_camera_1786276770175.jpg", "iphone17_camera.jpg", "Camera Close-up"),
    (r"C:\Users\NS\.gemini\antigravity\brain\c4a281be-c050-413d-b102-f7c4f2908e52\iphone17_side_1786276786970.jpg", "iphone17_side.jpg", "Side Titanium Profile"),
]

# Clear old gallery images for this product
ProductImage.objects.filter(product=product).delete()

for src, fname, alt in gallery_sources:
    if os.path.exists(src):
        dst = os.path.join(target_dir, fname)
        shutil.copy(src, dst)
        relative_path = f"products/gallery/{fname}"
        ProductImage.objects.create(
            product=product,
            image=relative_path,
            alt_text=alt
        )
        print(f"Added gallery image: {alt} -> {relative_path}")

print(f"Successfully attached {product.gallery_images.count()} matching gallery images to {product.name}!")
