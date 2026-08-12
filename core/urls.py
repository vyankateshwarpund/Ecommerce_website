from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('404/', views.error_404, name='preview_404'),
    path('403/', views.error_403, name='preview_403'),
    path('500/', views.error_500, name='preview_500'),
]
