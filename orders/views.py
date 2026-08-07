from django.shortcuts import render

def order_history(request):
    return render(request, 'orders/history.html')
