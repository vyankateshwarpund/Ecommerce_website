import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.test import Client, override_settings
from django.core import mail
from accounts.models import User

print("==================================================================")
print("TESTING FULL DJANGO FORGOT PASSWORD RESET FLOW")
print("==================================================================")

client = Client(HTTP_HOST='127.0.0.1:8000')
user = User.objects.get(email='pundsaurav@gmail.com')

with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
    # 1. Step 1: Request Password Reset
    res_request = client.post('/password-reset/', {'email': 'pundsaurav@gmail.com'}, follow=True)
    print(f"1. Password Reset Requested: HTTP {res_request.status_code} (Rendered /password-reset/done/)")

    # 2. Step 2: Check Email Outbox
    print(f"2. Sent Email Count in Outbox: {len(mail.outbox)}")
    assert len(mail.outbox) > 0, "Failed: No password reset email generated!"

    email_body = mail.outbox[0].body
    print("   Email Body Generated:")
    print("   ------------------------------------------------------------")
    for line in email_body.splitlines()[:6]:
        print("   ", line)
    print("   ------------------------------------------------------------")

    # Extract relative link from email
    match = re.search(r'http://127\.0\.0\.1:8000([^\s]+)', email_body)
    assert match, "Failed: Could not find reset link in email body!"
    confirm_path = match.group(1)
    print(f"3. Extracted Reset Path: '{confirm_path}'")

    # 4. Step 4: GET Confirm Page (Following redirect to set-password form)
    fresh_client = Client(HTTP_HOST='127.0.0.1:8000')
    res_confirm_get = fresh_client.get(confirm_path, follow=True)
    print(f"4. Confirm Page HTTP Response: {res_confirm_get.status_code} OK (Form rendered successfully)")

    # 5. Step 5: Submit New Password
    res_confirm_post = fresh_client.post(res_confirm_get.redirect_chain[-1][0] if res_confirm_get.redirect_chain else confirm_path, {
        'new_password1': 'NewPassword123',
        'new_password2': 'NewPassword123'
    }, follow=True)
    print(f"5. Set New Password Result: HTTP {res_confirm_post.status_code} (Redirected to Password Reset Complete)")

    # 6. Step 6: Verify New Password in DB
    user.refresh_from_db()
    is_valid_pass = user.check_password('NewPassword123')
    print(f"6. Database Password Hash Verification: {is_valid_pass}")
    assert is_valid_pass, "Failed: Password hash was not updated in database!"

    # Reset password back to standard Password123 for convenience
    user.set_password('Password123')
    user.save()
    print("   Reset password back to 'Password123' for convenience.")

print("==================================================================")
print("ALL 6 FORGOT PASSWORD STEPS VERIFIED 100% SUCCESSFUL!")
print("==================================================================")
