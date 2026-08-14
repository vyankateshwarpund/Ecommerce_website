import os
from django.core.management.base import BaseCommand
from products.models import Product, Brand, ProductImage
from categories.models import Category
from core.image_utils import compress_and_convert_to_webp

class Command(BaseCommand):
    help = 'Batch converts existing product, brand, and category images in media/ to optimized WebP format'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[*] Starting media batch conversion to WebP..."))
        converted_count = 0

        # 1. Convert Products main_image
        products = Product.objects.exclude(main_image='')
        for p in products:
            if p.main_image and hasattr(p.main_image, 'file'):
                if not p.main_image.name.lower().endswith('.webp'):
                    old_name = p.main_image.name
                    converted = compress_and_convert_to_webp(p.main_image, max_size=(1200, 1200))
                    if converted:
                        p.main_image.save(converted.name, converted, save=True)
                        self.stdout.write(self.style.SUCCESS(f"  + Converted Product: {p.name} ({old_name} -> {p.main_image.name})"))
                        converted_count += 1

        # 2. Convert Product Gallery Images
        gallery_images = ProductImage.objects.all()
        for g in gallery_images:
            if g.image and hasattr(g.image, 'file'):
                if not g.image.name.lower().endswith('.webp'):
                    old_name = g.image.name
                    converted = compress_and_convert_to_webp(g.image, max_size=(1200, 1200))
                    if converted:
                        g.image.save(converted.name, converted, save=True)
                        self.stdout.write(self.style.SUCCESS(f"  + Converted Gallery Image: {old_name} -> {g.image.name}"))
                        converted_count += 1

        # 3. Convert Brands
        brands = Brand.objects.exclude(logo='')
        for b in brands:
            if b.logo and hasattr(b.logo, 'file'):
                name_lower = b.logo.name.lower()
                if name_lower.endswith('.svg') or name_lower.endswith('.webp'):
                    continue
                old_name = b.logo.name
                converted = compress_and_convert_to_webp(b.logo, max_size=(600, 600))
                if converted:
                    b.logo.save(converted.name, converted, save=True)
                    self.stdout.write(self.style.SUCCESS(f"  + Converted Brand: {b.name} ({old_name} -> {b.logo.name})"))
                    converted_count += 1

        # 4. Convert Categories
        categories = Category.objects.exclude(image='')
        for c in categories:
            if c.image and hasattr(c.image, 'file'):
                name_lower = c.image.name.lower()
                if name_lower.endswith('.svg') or name_lower.endswith('.webp'):
                    continue
                old_name = c.image.name
                converted = compress_and_convert_to_webp(c.image, max_size=(800, 800))
                if converted:
                    c.image.save(converted.name, converted, save=True)
                    self.stdout.write(self.style.SUCCESS(f"  + Converted Category: {c.name} ({old_name} -> {c.image.name})"))
                    converted_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n[DONE] Conversion completed! {converted_count} images successfully optimized to WebP."))

