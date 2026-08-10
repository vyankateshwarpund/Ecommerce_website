import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client
from accounts.models import User, Address
from products.models import Product

print("==================================================================")
print("TESTING INVENTORY PROTECTION RULES (OUT OF STOCK & STOCK CAPPING)")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')
user = User.objects.get(email='pundsaurav@gmail.com')
client.force_login(user)

product = Product.objects.get(slug='apple-iphone-17-pro-max-cosmic-orange-256gb')
original_stock = product.stock

# ------------------------------------------------------------------
# TEST RULE 1: Out of Stock Block (stock = 0)
# ------------------------------------------------------------------
print("\n--- TEST RULE 1: Out of Stock Block ---")
product.stock = 0
product.save()

res1 = client.post(f'/cart/add/{product.id}/', {'quantity': 1}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
data1 = res1.json()
print("Out of Stock Add Attempt Result:")
print("Status:", data1.get('status'))
print("Message:", data1.get('message'))
assert data1.get('status') == 'error', "Failed: Out of stock product was allowed into cart!"
print("PASSED: Rule 1 - Out of stock products cannot be added or ordered!")

# ------------------------------------------------------------------
# TEST RULE 2: Stock Quantity Capping (stock = 3, requested = 10)
# ------------------------------------------------------------------
print("\n--- TEST RULE 2: Stock Quantity Capping ---")
product.stock = 3
product.save()

# Clear cart first
client.get('/cart/clear/')

res2 = client.post(f'/cart/add/{product.id}/', {'quantity': 10}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
data2 = res2.json()
print("Stock Capping Add Attempt Result (Requested: 10, Available: 3):")
print("Status:", data2.get('status'))
print("Cart Count:", data2.get('cart_count'))
print("Message:", data2.get('message'))
assert data2.get('cart_count') == 3, f"Failed: Cart count is {data2.get('cart_count')}, expected 3!"
print("PASSED: Rule 2 - Quantity automatically capped to available stock (3 units)!")

# Reset product stock back to original
product.stock = original_stock
product.save()
client.get('/cart/clear/')

print("\n==================================================================")
print("ALL INVENTORY PROTECTION RULES VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
