from django.shortcuts import render

def product_list(request):
    """Product list placeholder"""
    return render(request, 'products/list.html')
