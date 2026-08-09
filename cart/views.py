from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    total_mrp = cart.get_total_mrp()
    total_price = cart.get_total_price()
    savings = cart.get_total_savings()
    shipping_fee = 0 if total_price > 999 else (99 if total_price > 0 else 0)
    grand_total = total_price + shipping_fee

    context = {
        'cart': cart,
        'total_mrp': total_mrp,
        'total_price': total_price,
        'savings': savings,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Added "{product.name}" to your shopping cart!')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'success': True,
            'cart_count': len(cart),
            'message': f'Added {product.name} to cart!'
        })

    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, f'Updated quantity for "{product.name}".')
    else:
        cart.remove(product)
        messages.info(request, f'Removed "{product.name}" from your cart.')

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'Removed "{product.name}" from your cart.')
    return redirect('cart:cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, 'Your shopping cart has been cleared.')
    return redirect('cart:cart_detail')
