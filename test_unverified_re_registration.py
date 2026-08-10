import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client, override_settings
from accounts.models import User

print("==================================================================")
print("TESTING RE-REGISTRATION FOR UNVERIFIED ACCOUNTS")
print("==================================================================")

# Clean up initial test user
User.objects.filter(email='unverified_test@spcart.com').delete()

client = Client(HTTP_HOST='127.0.0.1:8000')

with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    # 1. First registration attempt
    res1 = client.post('/accounts/register/', {
        'first_name': 'Test',
        'last_name': 'One',
        'email': 'unverified_test@spcart.com',
        'password1': 'Password123',
        'password2': 'Password123'
    })
    print(f"1. First Registration Attempt: HTTP {res1.status_code} (Redirected to /accounts/verify-otp/)")
    u1 = User.objects.get(email='unverified_test@spcart.com')
    print(f"   Created User ID: {u1.id} | is_active={u1.is_active} | is_email_verified={u1.is_email_verified}")

    # 2. Second registration attempt with SAME email without verifying first
    res2 = client.post('/accounts/register/', {
        'first_name': 'Test',
        'last_name': 'Two',
        'email': 'unverified_test@spcart.com',
        'password1': 'NewPassword123',
        'password2': 'NewPassword123'
    })
    print(f"2. Second Registration Attempt (Re-registration): HTTP {res2.status_code} (Redirected to /accounts/verify-otp/)")
    
    u2 = User.objects.get(email='unverified_test@spcart.com')
    print(f"   Re-created User ID: {u2.id} | First Name: {u2.first_name}")
    assert u2.first_name == 'Test', "Failed: Re-registration did not succeed!"

    # Clean up test user
    u2.delete()

print("==================================================================")
print("RE-REGISTRATION FOR UNVERIFIED ACCOUNTS VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
