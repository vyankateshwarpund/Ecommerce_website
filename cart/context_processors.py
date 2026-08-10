from .cart import Cart

def cart_context(request):
    """Context processor providing cart and cart_count across all templates"""
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_count': len(cart)
    }

# Alias for compatibility with both 'cart' and 'cart_context' path references
cart = cart_context
