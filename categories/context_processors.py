from django.db.models import Count, Q
from django.core.cache import cache
from .models import Category

def categories_processor(request):
    categories = cache.get('all_categories_cached')
    if categories is None:
        categories = list(
            Category.objects.filter(is_active=True)
            .annotate(product_count=Count('products', filter=Q(products__is_available=True)))
            .order_by('order', 'name')
        )
        cache.set('all_categories_cached', categories, 300)
    return {
        'all_categories': categories
    }
