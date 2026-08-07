from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from categories.models import Category
from .models import Product, Brand

def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    filter_type = request.GET.get('filter')

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    if filter_type == 'deals':
        products = products.filter(is_deal=True)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def product_search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_available=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(brand__name__icontains=query)
        )

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)
