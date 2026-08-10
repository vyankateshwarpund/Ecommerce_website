from .models import WishlistItem

def wishlist_context(request):
    """Context processor providing wishlist_count across all templates"""
    if request.user.is_authenticated:
        count = WishlistItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}
