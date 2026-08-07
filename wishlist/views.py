from django.shortcuts import render

def wishlist_detail(request):
    return render(request, 'wishlist/wishlist.html')
