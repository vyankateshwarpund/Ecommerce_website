from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review

@login_required
def add_review_view(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()

        if rating and title and comment:
            review = Review.objects.filter(product=product, user=request.user).first()
            if review:
                review.rating = rating
                review.title = title
                review.comment = comment
                review.is_approved = True
                review.save()
                messages.success(request, f'Your review for "{product.name}" has been updated.')
            else:
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating,
                    title=title,
                    comment=comment,
                    is_approved=True
                )
                messages.success(request, f'Thank you for submitting your review for "{product.name}"!')

        return redirect('products:product_detail', slug=product.slug)

    return redirect('products:product_list')
