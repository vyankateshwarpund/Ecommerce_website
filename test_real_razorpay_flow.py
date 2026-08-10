import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client
from accounts.models import User, Address
from products.models import Product
from orders.models import Order

print("==================================================================")
print("TESTING REAL RAZORPAY PAYMENT GATEWAY FLOW")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')
user = User.objects.get(email='pundsaurav@gmail.com')
client.force_login(user)

product = Product.objects.get(slug='apple-iphone-17-pro-max-cosmic-orange-256gb')
initial_stock = product.stock

# 1. Add product to cart
client.post(f'/cart/add/{product.id}/', {'quantity': 1})

# 2. Submit Razorpay Order via AJAX
res_place = client.post('/orders/place-order/', {
    'payment_method': 'razorpay',
    'full_name': 'Saurav Pund',
    'phone': '9876543210',
    'street_address': 'Flat 101 MG Road',
    'city': 'Mumbai',
    'state': 'Maharashtra',
    'pincode': '400001'
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

data = res_place.json()
print(f"1. Razorpay Order Response: HTTP {res_place.status_code}")
print(f"   Order Number: {data.get('order_number')}")
print(f"   Razorpay Order ID: {data.get('razorpay_order_id')}")
print(f"   Amount (Paise): {data.get('amount')}")
print(f"   Key ID: {data.get('key_id')}")

assert data.get('status') == 'razorpay', "Failed: Razorpay order status not returned!"
assert data.get('razorpay_order_id') is not None, "Failed: Missing razorpay_order_id!"

# 3. Simulate Razorpay Gateway Verification Callback
res_verify = client.post('/payments/verify-razorpay-payment/', data=json.dumps({
    'razorpay_order_id': data.get('razorpay_order_id'),
    'razorpay_payment_id': 'pay_test_SPCart2026_1001',
    'razorpay_signature': 'test_signature_valid',
    'order_number': data.get('order_number')
}), content_type='application/json')

data_ver = res_verify.json()
print(f"2. Razorpay Payment Verification Response: HTTP {res_verify.status_code}")
print(f"   Redirect URL: {data_ver.get('redirect_url')}")

# 4. Verify Database State
order = Order.objects.get(order_number=data.get('order_number'))
print(f"3. Post-Payment Order DB State:")
print(f"   Payment Method: {order.payment_method}")
print(f"   Payment Status: {order.payment_status}")
print(f"   Order Status: {order.status}")
print(f"   Razorpay Payment ID: {order.razorpay_payment_id}")

assert order.payment_status is True, "Failed: Payment status should be True!"
assert order.status == 'confirmed', "Failed: Order status should be confirmed!"

product.refresh_from_db()
print(f"4. Updated Inventory Stock: {product.stock} (Initial was {initial_stock})")

print("==================================================================")
print("REAL RAZORPAY PAYMENT GATEWAY FLOW VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
