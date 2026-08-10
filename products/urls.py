from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('search/', views.product_search, name='product_search'),
    path('search/', views.product_search, name='search'),
    path('autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
