from django.shortcuts import render
from categories.models import Category
from products.models import Product, Brand

def home_view(request):
    featured_categories = Category.objects.filter(is_active=True, is_featured=True)[:6]
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:8]
    deal_products = Product.objects.filter(is_available=True, is_deal=True)[:2]
    brands = Brand.objects.filter(is_active=True, is_featured=True)[:6]

    context = {
        'featured_categories': featured_categories,
        'featured_products': featured_products,
        'deal_products': deal_products,
        'brands': brands,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    return render(request, 'core/contact.html')

def error_404(request, exception=None):
    return render(request, '404.html', status=404)

def error_403(request, exception=None):
    return render(request, '403.html', status=403)

def error_500(request):
    return render(request, '500.html', status=500)
