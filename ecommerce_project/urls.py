"""
ShopSphere — Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Core (Home, About, Contact)
    path('', include('core.urls')),

    # Accounts (Auth + Profile)
    path('accounts/', include('accounts.urls')),

    # Products & Categories
    path('products/', include('products.urls')),
    path('categories/', include('categories.urls')),

    # Shopping
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),

    # Orders & Payments
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),

    # Reviews
    path('reviews/', include('reviews.urls')),

    # Notifications
    path('notifications/', include('notifications.urls')),

    # Admin Dashboard (custom)
    path('dashboard/', include('dashboard.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Error Handlers
handler404 = 'core.views.error_404'
handler403 = 'core.views.error_403'
handler500 = 'core.views.error_500'
