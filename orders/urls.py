from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_history_view, name='history'),
    path('history/', views.order_history_view, name='order_history'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order_view, name='place_order'),
    path('success/<str:order_number>/', views.order_success_view, name='order_success'),
    path('detail/<str:order_number>/', views.order_detail_view, name='order_detail_alt'),
    path('<str:order_number>/', views.order_detail_view, name='order_detail'),
]
