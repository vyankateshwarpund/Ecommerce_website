from django.db import models
from django.conf import settings
from django.utils import timezone

class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M')} - {self.action}"


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=999.00)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(null=True, blank=True, help_text="Leave blank for no expiry")
    usage_limit = models.PositiveIntegerField(default=0, help_text="0 = unlimited uses")
    times_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% OFF)"

    def is_valid(self, order_amount=0):
        """Check if coupon is currently valid."""
        now = timezone.now()
        if not self.is_active:
            return False, 'This coupon is no longer active.'
        if now < self.valid_from:
            return False, 'This coupon is not valid yet.'
        if self.valid_to and now > self.valid_to:
            return False, 'This coupon has expired.'
        if self.usage_limit > 0 and self.times_used >= self.usage_limit:
            return False, 'This coupon has reached its usage limit.'
        if order_amount < float(self.min_order_amount):
            return False, f'Minimum order amount ₹{self.min_order_amount:.0f} required for this coupon.'
        return True, 'Valid'

    def calculate_discount(self, order_amount):
        """Calculate discount amount capped at max_discount_amount."""
        discount = (float(self.discount_percentage) / 100) * float(order_amount)
        return min(discount, float(self.max_discount_amount))
