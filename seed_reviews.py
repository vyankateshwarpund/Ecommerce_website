import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Product
from accounts.models import User
from reviews.models import Review

print("==================================================================")
print("SEEDING CUSTOMER REVIEWS & RATINGS FOR PRODUCTS")
print("==================================================================")

user = User.objects.filter(is_staff=True).first() or User.objects.first()
iphone = Product.objects.get(slug='apple-iphone-17-pro-max-cosmic-orange-256gb')

sample_reviews = [
    (iphone, 5, "Absolute Masterpiece! Cosmic Orange looks stunning!", "The build quality, camera clarity, and dynamic display on this iPhone 17 Pro Max are phenomenal. Battery easily lasts 2 full days!"),
    (iphone, 5, "Unbeatable Camera System & Performance", "The camera zoom and low-light portrait shots are studio grade. Highly recommended!"),
    (iphone, 4, "Premium flagship phone", "Amazing display and build. Cosmic Orange color is vibrant and unique."),
]

for prod, rat, title, comm in sample_reviews:
    Review.objects.get_or_create(
        product=prod,
        user=user,
        title=title,
        defaults={'rating': rat, 'comment': comm, 'is_approved': True}
    )

print("Customer reviews seeded successfully!")
print("==================================================================")
