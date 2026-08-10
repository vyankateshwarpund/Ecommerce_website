import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("==================================================================")
print("TESTING LIVE GMAIL SMTP EMAIL DISPATCH")
print("==================================================================")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

try:
    send_mail(
        subject='SPCart Gmail SMTP Test Email',
        message='Congratulations! Real Gmail SMTP integration is working successfully for SPCart.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['pundsaurav162@gmail.com', 'pundsaurav@gmail.com'],
        fail_silently=False,
    )
    print("✅ SUCCESS! Real email dispatched successfully via Gmail SMTP to your inbox!")
except Exception as e:
    print(f"❌ SMTP Error: {e}")

print("==================================================================")
