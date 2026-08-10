import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("==================================================================")
print("TESTING GMAIL SMTP WITH EMAIL: pundsaurav@gmail.com")
print("==================================================================")

# Override EMAIL_HOST_USER temporarily to test pundsaurav@gmail.com
settings.EMAIL_HOST_USER = 'pundsaurav@gmail.com'
settings.DEFAULT_FROM_EMAIL = 'SPCart Support <pundsaurav@gmail.com>'

try:
    send_mail(
        subject='SPCart Gmail SMTP Test Email',
        message='Congratulations! Real Gmail SMTP integration is working successfully for SPCart.',
        from_email='pundsaurav@gmail.com',
        recipient_list=['pundsaurav@gmail.com', 'pundsaurav162@gmail.com'],
        fail_silently=False,
    )
    print("SUCCESS! Real email dispatched successfully via Gmail SMTP to your inbox!")
except Exception as e:
    print(f"SMTP Error: {e}")

print("==================================================================")
