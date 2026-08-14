from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_html_email(subject, template_name, context, recipient_list):
    """Sends HTML email rendered from template with plain-text fallback"""
    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'SPCart Team <pundsaurav@gmail.com>')

        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        return True
    except Exception as e:
        print(f"Error sending email '{subject}': {e}")
        return False

def send_welcome_email(user):
    subject = "Welcome to SPCart! 🎉"
    context = {'user': user}
    return send_html_email(subject, 'emails/welcome_email.html', context, [user.email])

def send_order_confirmation_email(order):
    subject = f"🎉 Order Confirmed - #{order.order_number} | SPCart"
    context = {'order': order}
    return send_html_email(subject, 'emails/order_confirmation_email.html', context, [order.user.email])

def send_shipping_notification_email(order):
    subject = f"🚚 Order Shipped - #{order.order_number} | SPCart"
    context = {'order': order}
    return send_html_email(subject, 'emails/shipping_notification_email.html', context, [order.user.email])

def send_delivery_notification_email(order):
    subject = f"📦 Order Delivered Successfully - #{order.order_number} | SPCart"
    context = {'order': order}
    return send_html_email(subject, 'emails/order_delivered_email.html', context, [order.user.email])

def send_cancellation_notification_email(order):
    subject = f"Order Cancelled - #{order.order_number} | SPCart"
    context = {'order': order}
    return send_html_email(subject, 'emails/order_cancelled_email.html', context, [order.user.email])

def notify_order_status_change(order, status):
    """
    Unified helper to send BOTH In-App Notification AND HTML Email
    whenever an order status changes (confirmed, shipped, delivered, cancelled).
    """
    from notifications.models import Notification

    status_titles = {
        'confirmed': (f"Order Confirmed #{order.order_number}", f"Your order #{order.order_number} for ₹{order.total_amount:.0f} has been confirmed!"),
        'processing': (f"Order Processing #{order.order_number}", f"Your order #{order.order_number} is currently being packed."),
        'shipped': (f"Order Shipped #{order.order_number}", f"Great news! Order #{order.order_number} has been shipped and is on its way."),
        'delivered': (f"Order Delivered #{order.order_number}", f"Your order #{order.order_number} has been delivered successfully!"),
        'cancelled': (f"Order Cancelled #{order.order_number}", f"Order #{order.order_number} has been cancelled."),
    }

    title, msg = status_titles.get(status, (f"Order Update #{order.order_number}", f"Order #{order.order_number} status updated to {status}."))

    # 1. Create In-App Notification
    try:
        Notification.objects.create(
            user=order.user,
            title=title,
            message=msg,
            notification_type='order',
            link_url=f"/orders/{order.order_number}/"
        )
    except Exception as e:
        print(f"Error creating notification: {e}")

    # 2. Dispatch Email
    try:
        if status in ['confirmed', 'pending']:
            send_order_confirmation_email(order)
        elif status == 'shipped':
            send_shipping_notification_email(order)
        elif status == 'delivered':
            send_delivery_notification_email(order)
        elif status == 'cancelled':
            send_cancellation_notification_email(order)
    except Exception as e:
        print(f"Error dispatching order status email: {e}")
