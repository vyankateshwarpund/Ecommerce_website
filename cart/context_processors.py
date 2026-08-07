def cart_context(request):
    """Context processor providing cart_count across all templates"""
    return {'cart_count': 0}
