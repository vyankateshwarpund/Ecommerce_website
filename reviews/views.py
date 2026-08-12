from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from orders.models import OrderItem
from .models import Review

@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Requirement: Check if user purchased product
    has_purchased = OrderItem.objects.filter(order__user=request.user, product=product).exists()
    
    if not has_purchased and not request.user.is_staff:
        messages.error(request, f'You can only review "{product.name}" after purchasing it!')
        return redirect('products:product_detail', slug=product.slug)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()

        if rating and title and comment:
            review, created = Review.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating, 'title': title, 'comment': comment, 'is_approved': True}
            )
            if not created:
                review.rating = rating
                review.title = title
                review.comment = comment
                review.is_approved = True
                review.save()
                messages.success(request, f'Your review for "{product.name}" has been updated.')
            else:
                messages.success(request, f'Thank you for reviewing "{product.name}"!')

        return redirect('products:product_detail', slug=product.slug)

    return redirect('products:product_detail', slug=product.slug)


@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.info(request, 'Your review has been deleted.')
    return redirect('products:product_detail', slug=product_slug)
