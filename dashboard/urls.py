from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('products/', views.products_list, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('customers/', views.customers_list, name='customers'),
    path('categories/', views.categories_list, name='categories'),
    path('reviews/', views.reviews_list, name='reviews'),
    path('reviews/<int:review_id>/toggle/', views.toggle_review_status, name='toggle_review_status'),
    path('coupons/', views.coupons_list, name='coupons'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('export/<str:report_type>/', views.export_reports, name='export_reports'),
    path('activity-log/', views.activity_log_view, name='activity_log'),
]
