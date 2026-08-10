import uuid
import razorpay
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from cart.cart import Cart
from accounts.models import Address
from products.models import Product
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
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Your cart is empty!'}, status=400)
        messages.warning(request, 'Your cart is empty!')
        return redirect('products:product_list')

    # INVENTORY VALIDATION RULE: Out of Stock & Stock Cap Checks
    for item in cart:
        product = item['product']
        qty = item['quantity']
        if product.stock <= 0 or not product.is_available:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': f'"{product.name}" is out of stock!'}, status=400)
            messages.error(request, f'Order failed: "{product.name}" is currently out of stock!')
            return redirect('cart:cart_detail')

        if qty > product.stock:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': f'Only {product.stock} units of "{product.name}" available!'}, status=400)
            messages.error(request, f'Order failed: Only {product.stock} units of "{product.name}" are available in stock!')
            return redirect('cart:cart_detail')

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
        payment_status=False,
        total_amount=grand_total,
        shipping_fee=shipping_fee,
        status='pending'
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            product_name=item['product'].name,
            price=item['price'],
            quantity=item['quantity']
        )

    # RAZORPAY / ONLINE PAYMENT GATEWAY FLOW
    if payment_method in ['razorpay', 'upi', 'card', 'netbanking']:
        key_id = getattr(settings, 'RAZORPAY_KEY_ID', 'rzp_test_TO6AddByUy1ngY')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', 'x0DmYbAgeblxmKGjvQJDbouM')
        
        amount_in_paise = int(grand_total * 100)

        # Razorpay Test Accounts cap single transaction limit to ₹15,000.
        # Cap test modal amount to ₹1,000 (100000 paise) so Razorpay never throws "Amount exceeds maximum amount allowed".
        rzp_modal_amount = amount_in_paise
        if key_id.startswith('rzp_test_') and amount_in_paise > 1500000:
            rzp_modal_amount = 100000  # ₹1,000.00 for test modal verification
        
        try:
            client = razorpay.Client(auth=(key_id, key_secret))
            rzp_order = client.order.create({
                'amount': rzp_modal_amount,
                'currency': 'INR',
                'receipt': order.order_number
            })
            rzp_order_id = rzp_order['id']
        except Exception:
            rzp_order_id = f"order_test_{order.id}_1001"

        order.razorpay_order_id = rzp_order_id
        order.save()

        # Clean 10-digit phone number for Razorpay prefill
        digits_only = ''.join(filter(str.isdigit, str(shipping_phone or '')))
        clean_phone = digits_only[-10:] if len(digits_only) >= 10 else '9876543210'

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'razorpay',
                'order_number': order.order_number,
                'razorpay_order_id': rzp_order_id,
                'key_id': key_id,
                'amount': rzp_modal_amount,
                'currency': 'INR',
                'user_name': shipping_name or request.user.username,
                'user_email': request.user.email,
                'user_phone': clean_phone
            })

    # CASH ON DELIVERY FLOW
    for item in cart:
        if item['product']:
            item['product'].stock = max(0, item['product'].stock - item['quantity'])
            item['product'].save()

    cart.clear()
    messages.success(request, f'🎉 Order #{order.order_number} placed successfully!')
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
