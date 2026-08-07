def wishlist_context(request):
    """Context processor providing wishlist_count across all templates"""
    return {'wishlist_count': 0}
