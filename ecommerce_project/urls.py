"""
ShopSphere — Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Password Reset Top-Level Endpoints
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
        email_template_name="accounts/password_reset_email.txt",
        html_email_template_name="accounts/password_reset_email.html",
        subject_template_name="accounts/password_reset_subject.txt",
        success_url="/password-reset/done/"
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
        post_reset_login=True,
        post_reset_login_backend='django.contrib.auth.backends.ModelBackend',
        success_url="/password-reset-complete/"
    ), name="password_reset_confirm"),

    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name="password_reset_complete"),

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
