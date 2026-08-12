from django.db import models
from django.conf import settings
from django.db.models import Avg
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    title = models.CharField(max_length=255)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.rating}★ Review for {self.product.name} by {self.user.email}"

    def update_product_rating(self):
        avg_rating = Review.objects.filter(product=self.product, is_approved=True).aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            self.product.rating = round(float(avg_rating), 1)
        else:
            self.product.rating = 4.9
        self.product.save(update_fields=['rating'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        avg_rating = Review.objects.filter(product=product, is_approved=True).aggregate(Avg('rating'))['rating__avg']
        product.rating = round(float(avg_rating), 1) if avg_rating else 4.9
        product.save(update_fields=['rating'])
