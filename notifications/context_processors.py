def notifications_context(request):
    """Context processor providing unread notifications count"""
    return {'unread_notifications_count': 0}
