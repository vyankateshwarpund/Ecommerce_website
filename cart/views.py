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
    requested_qty = int(request.POST.get('quantity', 1))

    # Rule 1: Out of Stock Protection
    if product.stock <= 0 or not product.is_available:
        msg = f'Sorry, "{product.name}" is currently out of stock!'
        messages.error(request, msg)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'success': False, 'message': msg})
        return redirect('products:product_list')

    # Existing quantity in cart
    existing_qty = cart.cart.get(str(product.id), {}).get('quantity', 0)
    total_requested = existing_qty + requested_qty

    # Rule 2: Stock Quantity Capping
    if total_requested > product.stock:
        allowed_add = max(0, product.stock - existing_qty)
        if allowed_add > 0:
            cart.add(product=product, quantity=allowed_add)
            msg = f'Only {product.stock} units of "{product.name}" in stock. Quantity updated to {product.stock} units.'
            messages.warning(request, msg)
        else:
            msg = f'You already have the maximum available stock ({product.stock} units) of "{product.name}" in your cart.'
            messages.warning(request, msg)
    else:
        cart.add(product=product, quantity=requested_qty)
        msg = f'Added "{product.name}" to your shopping cart!'
        messages.success(request, msg)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'success': True,
            'cart_count': len(cart),
            'message': msg
        })

    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    requested_qty = int(request.POST.get('quantity', 1))

    # Rule 2: Stock Quantity Capping during update
    if requested_qty > product.stock:
        requested_qty = product.stock
        messages.warning(request, f'Capped "{product.name}" quantity to available stock ({product.stock} units).')

    if requested_qty > 0 and product.stock > 0:
        cart.add(product=product, quantity=requested_qty, override_quantity=True)
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
