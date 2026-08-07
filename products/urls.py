from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Search view placeholder for navbar form
    path('search/', views.product_list, name='search'),
    path('', views.product_list, name='product_list'),
]
