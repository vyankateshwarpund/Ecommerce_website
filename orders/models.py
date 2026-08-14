from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import Address

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Order Placed'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('razorpay', 'Razorpay Online (UPI / Card / NetBanking)'),
        ('upi', 'UPI Direct'),
        ('card', 'Credit / Debit Card'),
        ('netbanking', 'Net Banking'),
    )

    STEPS_ORDER = ['pending', 'confirmed', 'processing', 'shipped', 'out_for_delivery', 'delivered']

    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    
    # Shipping Info
    shipping_name = models.CharField(max_length=255)
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=20)

    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False, help_text="For COD order verification")
    confirmed_at = models.DateTimeField(null=True, blank=True)

    # Razorpay Transaction Identifiers
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.email}"

    @property
    def full_name(self):
        return self.shipping_name

    @property
    def address_line_1(self):
        return self.shipping_address

    @property
    def city(self):
        return self.shipping_city

    @property
    def pincode(self):
        return self.shipping_pincode

    @property
    def current_step_index(self):
        try:
            return self.STEPS_ORDER.index(self.status)
        except ValueError:
            return -1 if self.status == 'cancelled' else 0

    @property
    def is_cancelled(self):
        return self.status == 'cancelled'

    @property
    def is_cancellable(self):
        return self.status in ['pending', 'confirmed']

    @property
    def progress_percentage(self):
        if self.status == 'cancelled':
            return 0
        total_steps = len(self.STEPS_ORDER) - 1
        idx = max(0, self.current_step_index)
        return int((idx / total_steps) * 100)

    @property
    def estimated_delivery_date(self):
        from datetime import timedelta
        return self.created_at + timedelta(days=3)

    @property
    def tracking_number(self):
        clean_num = ''.join(c for c in self.order_number if c.isalnum())
        return f"SPC-TRK-{clean_num[-8:]}"

    @property
    def tracking_steps(self):
        steps_meta = [
            {
                'key': 'pending',
                'title': 'Order Placed',
                'desc': 'We have received your order.',
                'icon': 'fa-clipboard-check',
            },
            {
                'key': 'confirmed',
                'title': 'Confirmed',
                'desc': 'Order verified and confirmed.',
                'icon': 'fa-circle-check',
            },
            {
                'key': 'processing',
                'title': 'Processing',
                'desc': 'Items packed & ready for courier.',
                'icon': 'fa-box-open',
            },
            {
                'key': 'shipped',
                'title': 'Shipped',
                'desc': 'In transit with logistics partner.',
                'icon': 'fa-truck-fast',
            },
            {
                'key': 'out_for_delivery',
                'title': 'Out for Delivery',
                'desc': 'Agent out for delivery to your address.',
                'icon': 'fa-motorcycle',
            },
            {
                'key': 'delivered',
                'title': 'Delivered',
                'desc': 'Package delivered successfully.',
                'icon': 'fa-house-circle-check',
            },
        ]
        curr_idx = self.current_step_index
        for idx, step in enumerate(steps_meta):
            if self.is_cancelled:
                step['state'] = 'cancelled'
            elif idx < curr_idx:
                step['state'] = 'completed'
            elif idx == curr_idx:
                step['state'] = 'active'
            else:
                step['state'] = 'upcoming'
        return steps_meta


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order #{self.order.order_number}"

    @property
    def total_price(self):
        return self.price * self.quantity


class BulkOrderInquiry(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('contacted', 'Contacted / In Discussion'),
        ('quoted', 'Quote Sent'),
        ('completed', 'Completed'),
        ('cancelled', 'Closed / Rejected'),
    )

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200, blank=True)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=10)
    target_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Total budget in INR")
    delivery_pincode = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Bulk Order Inquiries'

    def __str__(self):
        return f"Bulk #{self.id} - {self.product_name} ({self.quantity} units) from {self.name}"

