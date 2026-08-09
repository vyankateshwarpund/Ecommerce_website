import uuid
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from accounts.models import Address
from .models import Order, OrderItem

@login_required
def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty! Add products before checking out.')
        return redirect('products:product_list')

    addresses = Address.objects.filter(user=request.user)
    
    # Auto-create saved address from last order if user has no saved addresses
    if not addresses.exists():
        last_order = Order.objects.filter(user=request.user).first()
        if last_order:
            Address.objects.create(
                user=request.user,
                full_name=last_order.shipping_name,
                phone=last_order.shipping_phone,
                address_line=last_order.shipping_address,
                area=last_order.shipping_city,
                city=last_order.shipping_city,
                state=last_order.shipping_state,
                postal_code=last_order.shipping_pincode,
                is_default=True
            )
            addresses = Address.objects.filter(user=request.user)

    default_address = addresses.filter(is_default=True).first() or addresses.first()
    
    total_price = cart.get_total_price()
    shipping_fee = 0 if total_price > 999 else (99 if total_price > 0 else 0)
    grand_total = total_price + shipping_fee

    context = {
        'cart': cart,
        'addresses': addresses,
        'default_address': default_address,
        'total_price': total_price,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def place_order_view(request):
    if request.method != 'POST':
        return redirect('orders:checkout')

    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:product_list')

    address_id = request.POST.get('address_id')
    payment_method = request.POST.get('payment_method', 'cod')

    if address_id:
        addr = get_object_or_404(Address, id=address_id, user=request.user)
        shipping_name = addr.full_name
        shipping_phone = addr.phone
        shipping_address = addr.address_line
        shipping_city = addr.city
        shipping_state = addr.state
        shipping_pincode = addr.postal_code
    else:
        shipping_name = request.POST.get('full_name')
        shipping_phone = request.POST.get('phone')
        shipping_address = request.POST.get('street_address')
        shipping_city = request.POST.get('city')
        shipping_state = request.POST.get('state')
        shipping_pincode = request.POST.get('pincode')

        # Save new address for future orders using exact Address model fields
        if shipping_name and shipping_address:
            Address.objects.create(
                user=request.user,
                full_name=shipping_name,
                phone=shipping_phone,
                address_line=shipping_address,
                area=shipping_city,
                city=shipping_city,
                state=shipping_state,
                postal_code=shipping_pincode,
                is_default=not Address.objects.filter(user=request.user).exists()
            )

    total_price = cart.get_total_price()
    shipping_fee = 0 if total_price > 999 else (99 if total_price > 0 else 0)
    grand_total = total_price + shipping_fee

    # Generate unique order number
    order_number = f"SPC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    order = Order.objects.create(
        order_number=order_number,
        user=request.user,
        shipping_name=shipping_name,
        shipping_phone=shipping_phone,
        shipping_address=shipping_address,
        shipping_city=shipping_city,
        shipping_state=shipping_state,
        shipping_pincode=shipping_pincode,
        payment_method=payment_method,
        payment_status=True if payment_method != 'cod' else False,
        total_amount=grand_total,
        shipping_fee=shipping_fee,
        status='pending'
    )

    # Create Order Items
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            product_name=item['product'].name,
            price=item['price'],
            quantity=item['quantity']
        )

    # Clear Session Cart
    cart.clear()

    messages.success(request, f'🎉 Congratulations! Your Order #{order.order_number} has been placed successfully!')
    return redirect('orders:order_success', order_number=order.order_number)


@login_required
def order_success_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
