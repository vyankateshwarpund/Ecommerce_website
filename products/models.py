import os
from django.db import models
from django.utils.text import slugify
from categories.models import Category

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def has_logo(self):
        """Returns True only if the logo file actually exists on disk."""
        try:
            return bool(self.logo and self.logo.name and os.path.exists(self.logo.path))
        except Exception:
            return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.logo and hasattr(self.logo, 'file') and not self.logo.name.lower().endswith('.webp'):
            try:
                from core.image_utils import compress_and_convert_to_webp
                converted = compress_and_convert_to_webp(self.logo, max_size=(600, 600))
                if converted:
                    self.logo.save(converted.name, converted, save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)



class Product(models.Model):
    BADGE_CHOICES = (
        ('bestseller', 'Best Seller'),
        ('new', 'New Arrival'),
        ('trending', 'Trending'),
        ('limited', 'Limited Stock'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=10)
    
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_deal = models.BooleanField(default=False)
    
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    reviews_count = models.PositiveIntegerField(default=0)
    
    main_image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.main_image and hasattr(self.main_image, 'file') and not self.main_image.name.lower().endswith('.webp'):
            try:
                from core.image_utils import compress_and_convert_to_webp
                converted = compress_and_convert_to_webp(self.main_image, max_size=(1200, 1200))
                if converted:
                    self.main_image.save(converted.name, converted, save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.discount_price and self.price > 0:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return int(round(discount))
        return 0

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def in_stock(self):
        return self.stock > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gallery image for {self.product.name}"

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file') and not self.image.name.lower().endswith('.webp'):
            try:
                from core.image_utils import compress_and_convert_to_webp
                converted = compress_and_convert_to_webp(self.image, max_size=(1200, 1200))
                if converted:
                    self.image.save(converted.name, converted, save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)

