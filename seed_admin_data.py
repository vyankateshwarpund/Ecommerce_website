import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from dashboard.models import Coupon, ActivityLog
from accounts.models import User

admin_user = User.objects.filter(is_staff=True).first()

# 1. Coupons
c1, _ = Coupon.objects.get_or_create(code='SPCART10', defaults={'discount_percentage': 10.00, 'min_order_amount': 999.00, 'max_discount_amount': 500.00})
c2, _ = Coupon.objects.get_or_create(code='WELCOME20', defaults={'discount_percentage': 20.00, 'min_order_amount': 1999.00, 'max_discount_amount': 1000.00})

# 2. Activity Logs
logs = [
    ("Updated product stock for Apple iPhone 17 Pro Max", "Stock increased by +10 units"),
    ("Changed Order #SPC-20260809-144C92 status to Shipped", "Courier partner: BlueDart Express"),
    ("Created new discount coupon 'SPCART10'", "10% OFF on minimum order ₹999"),
    ("Approved customer review for Ergonomic Mesh Office Chair", "5 Star Rating by Amit K."),
]

for act, det in logs:
    ActivityLog.objects.get_or_create(action=act, defaults={'user': admin_user, 'details': det})

print("Admin coupons and activity log seeded successfully!")
