from django.db import models
from django.utils.text import slugify
from django.core.cache import cache

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fas fa-folder', help_text='Font Awesome icon class')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.image and hasattr(self.image, 'file') and not self.image.name.lower().endswith('.webp'):
            try:
                from core.image_utils import compress_and_convert_to_webp
                converted = compress_and_convert_to_webp(self.image, max_size=(800, 800))
                if converted:
                    self.image.save(converted.name, converted, save=False)
            except Exception:
                pass
        super().save(*args, **kwargs)
        cache.delete('all_categories_cached')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('all_categories_cached')
