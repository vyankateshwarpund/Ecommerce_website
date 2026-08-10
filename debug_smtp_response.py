import os
import smtplib
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("==================================================================")
print("VERBOSE GMAIL SMTP DIAGNOSTIC TEST")
print("==================================================================")

# Enable SMTP verbose debugging to print full TLS conversation with Google
connection = django.core.mail.get_connection()
connection.open()
connection.connection.set_debuglevel(1)

try:
    message_count = connection.send_messages([
        django.core.mail.EmailMessage(
            subject='[SPCart] Immediate Password Reset Notification',
            body='Hello Saurav,\n\nThis is your live SPCart password reset test notification.\n\nLink: http://127.0.0.1:8000/password-reset-confirm/MQ/test-token/\n\nThanks,\nSPCart Team',
            from_email='SPCart Support <pundsaurav@gmail.com>',
            to=['pundsaurav@gmail.com', 'sauravpund162@gmail.com'],
            connection=connection
        )
    ])
    print(f"\n✅ Sent {message_count} message(s) via Google SMTP!")
except Exception as e:
    print(f"\n❌ Error during email dispatch: {e}")
finally:
    connection.close()

print("==================================================================")
