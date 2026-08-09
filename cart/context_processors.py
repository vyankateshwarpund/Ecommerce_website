from .cart import Cart

def cart_context(request):
    """Context processor providing cart and cart_count across all templates"""
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': len(cart)
    }
