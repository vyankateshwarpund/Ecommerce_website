from django.shortcuts import render

def home(request):
    """Home Page View"""
    return render(request, 'core/home.html')

def about(request):
    """About Us View"""
    return render(request, 'core/about.html')

def contact(request):
    """Contact View"""
    return render(request, 'core/contact.html')

def error_404(request, exception=None):
    """Custom 404 handler"""
    return render(request, '404.html', status=404)

def error_403(request, exception=None):
    """Custom 403 handler"""
    return render(request, '403.html', status=403)

def error_500(request):
    """Custom 500 handler"""
    return render(request, '500.html', status=500)
