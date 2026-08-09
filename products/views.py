from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from categories.models import Category
from .models import Product, Brand

def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    brands = Brand.objects.filter(is_active=True).order_by('name')

    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    filter_type = request.GET.get('filter')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')
    min_rating = request.GET.get('min_rating')
    sort_by = request.GET.get('sort', 'default')

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    if filter_type == 'deals':
        products = products.filter(is_deal=True)
    elif filter_type == 'featured':
        products = products.filter(is_featured=True)

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if in_stock == '1':
        products = products.filter(stock__gt=0)

    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    # Sorting
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-is_featured', '-id')

    # Pagination (12 items per page)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'total_count': products.count(),
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': brand_slug,
        'sort_by': sort_by,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'in_stock': in_stock or '',
        'min_rating': min_rating or '',
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # 1. Fetch products in same category
    related_products = list(Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4])
    
    # 2. Fallback if fewer than 4 items in same category: populate from other available products
    if len(related_products) < 4:
        needed = 4 - len(related_products)
        existing_ids = [p.id for p in related_products] + [product.id]
        other_products = Product.objects.filter(is_available=True).exclude(id__in=existing_ids)[:needed]
        related_products.extend(list(other_products))

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
        'total_count': products.count(),
    }
    return render(request, 'products/search_results.html', context)
