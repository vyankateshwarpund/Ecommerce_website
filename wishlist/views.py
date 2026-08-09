from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product
from .models import WishlistItem

@login_required
def wishlist_detail(request):
    items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': items})


@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        item.delete()
        added = False
        message = f'Removed "{product.name}" from your wishlist.'
    else:
        added = True
        message = f'Saved "{product.name}" to your wishlist!'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'success': True,
            'added': added,
            'in_wishlist': added,
            'message': message,
            'wishlist_count': WishlistItem.objects.filter(user=request.user).count()
        })

    messages.info(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:wishlist_detail'))
