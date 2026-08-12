from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:order_id>/', views.order_detail_staff, name='order_detail_staff'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
    path('products/', views.products_list, name='products'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('customers/', views.customers_list, name='customers'),
    path('customers/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('customers/<int:user_id>/delete/', views.customer_delete, name='customer_delete'),
    path('categories/', views.categories_list, name='categories'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    path('brands/', views.brands_list, name='brands'),
    path('brands/<int:brand_id>/delete/', views.brand_delete, name='brand_delete'),
    path('reviews/', views.reviews_list, name='reviews'),
    path('reviews/<int:review_id>/toggle/', views.toggle_review_status, name='toggle_review_status'),
    path('reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path('coupons/', views.coupons_list, name='coupons'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('export/<str:report_type>/', views.export_reports, name='export_reports'),
    path('activity-log/', views.activity_log_view, name='activity_log'),
]
