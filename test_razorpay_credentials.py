import os
import razorpay
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.conf import settings

print("==================================================================")
print("TESTING USER'S REAL RAZORPAY TEST KEYS")
print("==================================================================")

key_id = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_TO6AddByUy1ngY')
key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', 'x0DmYbAgeblxmKGjvQJDbouM')

print(f"Key ID being tested: {key_id}")

try:
    client = razorpay.Client(auth=(key_id, key_secret))
    order = client.order.create({
        'amount': 50000, # ₹500.00
        'currency': 'INR',
        'receipt': 'test_rcpt_1001'
    })
    print("\nSUCCESS! Real Razorpay Test Order Created Successfully!")
    print(f"   Razorpay Order ID: {order['id']}")
    print(f"   Amount: RS {order['amount'] / 100}")
    print(f"   Status: {order['status']}")
except Exception as e:
    print(f"\nRazorpay API Error: {e}")

print("==================================================================")
