import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client
from accounts.models import User
from products.models import Product
from orders.models import Order

print("==================================================================")
print("TESTING DEDICATED UPI & QR CODE PAYMENT FLOW")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')
user = User.objects.get(email='pundsaurav@gmail.com')
client.force_login(user)

product = Product.objects.get(slug='apple-iphone-17-pro-max-cosmic-orange-256gb')

# 1. Add item to cart
client.post(f'/cart/add/{product.id}/', {'quantity': 1})

# 2. Place order with UPI & QR Payment Option
res = client.post('/orders/place-order/', {
    'payment_method': 'upi',
    'full_name': 'Saurav Pund',
    'phone': '9876543210',
    'street_address': 'Flat 101 MG Road',
    'city': 'Mumbai',
    'state': 'Maharashtra',
    'pincode': '400001'
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

data = res.json()
print(f"1. UPI Order Creation Response: HTTP {res.status_code}")
print(f"   Order Number: {data.get('order_number')}")
print(f"   Amount: RS {data.get('amount') / 100}")

assert data.get('status') == 'razorpay', "Failed: Order status should be razorpay!"

# 3. Simulate UPI QR Scan Verification
res_verify = client.post('/payments/verify-razorpay-payment/', data=json.dumps({
    'razorpay_order_id': data.get('razorpay_order_id'),
    'razorpay_payment_id': 'pay_upi_qr_1001',
    'razorpay_signature': 'sig_upi_valid',
    'order_number': data.get('order_number')
}), content_type='application/json')

data_ver = res_verify.json()
print(f"2. UPI QR Verification Response: HTTP {res_verify.status_code}")
print(f"   Redirect URL: {data_ver.get('redirect_url')}")

order = Order.objects.get(order_number=data.get('order_number'))
print(f"3. DB Order Status: Payment Method = {order.payment_method} | Paid = {order.payment_status} | Status = {order.status}")
assert order.payment_status is True, "Failed: Payment status should be True!"

print("==================================================================")
print("ALL UPI & QR CODE PAYMENT STEPS VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
