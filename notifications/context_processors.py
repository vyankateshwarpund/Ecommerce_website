from .models import Notification

def notification_context(request):
    """Context processor providing unread_notifications_count across all templates"""
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        count = 0
    return {'unread_notifications_count': count}
