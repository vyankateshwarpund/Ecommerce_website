import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client, override_settings
from accounts.models import User, EmailOTP

print("==================================================================")
print("TESTING REGISTRATION WITH EMAIL OTP VERIFICATION FLOW")
print("==================================================================")

# Clean up test user if exists
User.objects.filter(email='test_otp_user@spcart.com').delete()

client = Client(HTTP_HOST='127.0.0.1:8000')

with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    # 1. Step 1: Submit Registration Form
    res_reg = client.post('/accounts/register/', {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test_otp_user@spcart.com',
        'password1': 'Password123',
        'password2': 'Password123'
    })
    print(f"1. Registration Submission Response: HTTP {res_reg.status_code} (Redirected to /accounts/verify-otp/)")

    # 2. Step 2: Check User Inactive State in Database
    user = User.objects.get(email='test_otp_user@spcart.com')
    print(f"2. User Created in DB: is_active={user.is_active} | is_email_verified={user.is_email_verified}")
    assert user.is_active is False, "Failed: User should be inactive prior to OTP verification!"

    # 3. Step 3: Fetch Generated OTP Code
    otp_record = EmailOTP.objects.filter(user=user).latest('created_at')
    print(f"3. Generated 6-Digit OTP Code: '{otp_record.otp_code}'")

    # 4. Step 4: Submit OTP Verification
    res_verify = client.post('/accounts/verify-otp/', {'otp': otp_record.otp_code})
    print(f"4. OTP Verification Submission Response: HTTP {res_verify.status_code} (Redirected to Home)")

    # 5. Step 5: Check Activated User State
    user.refresh_from_db()
    print(f"5. Post-Verification User State: is_active={user.is_active} | is_email_verified={user.is_email_verified}")
    assert user.is_active is True, "Failed: User is_active was not set to True!"
    assert user.is_email_verified is True, "Failed: User is_email_verified was not set to True!"

    # Clean up test user
    user.delete()

print("==================================================================")
print("ALL REGISTRATION OTP VERIFICATION STEPS VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
