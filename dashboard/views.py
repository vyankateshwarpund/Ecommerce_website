import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from orders.models import Order, OrderItem
from products.models import Product, Brand
from categories.models import Category
from accounts.models import User, Profile, Address
from reviews.models import Review
from .models import ActivityLog, Coupon

@staff_member_required
def index(request):
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_users = User.objects.count()

    recent_orders = Order.objects.order_by('-created_at')[:8]
    low_stock_products = Product.objects.filter(stock__lte=5, is_available=True)
    activity_logs = ActivityLog.objects.all()[:5]

    # Best Sellers
    best_sellers = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(total_sold__gt=0).order_by('-total_sold')[:5]

    # Notifications count
    out_of_stock_count = Product.objects.filter(stock=0).count()
    low_stock_count = low_stock_products.count()
    new_orders_count = Order.objects.filter(status='pending').count()
    total_notifications = out_of_stock_count + low_stock_count + new_orders_count

    # Chart.js Dataset: Monthly Revenue (Database Portable)
    monthly_sales = Order.objects.values('created_at__year', 'created_at__month').annotate(total=Sum('total_amount')).order_by('created_at__year', 'created_at__month')
    chart_months = [f"{m['created_at__month']}/{m['created_at__year']}" for m in monthly_sales]
    chart_revenue = [float(m['total']) for m in monthly_sales]

    # Chart.js Dataset: Order Status Breakdown
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    status_dict = dict(Order.STATUS_CHOICES)
    status_labels = [status_dict.get(s['status'], s['status']) for s in status_counts]
    status_values = [s['count'] for s in status_counts]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'best_sellers': best_sellers,
        'activity_logs': activity_logs,
        'out_of_stock_count': out_of_stock_count,
        'low_stock_count': low_stock_count,
        'new_orders_count': new_orders_count,
        'total_notifications': total_notifications,
        'chart_months': chart_months,
        'chart_revenue': chart_revenue,
        'status_labels': status_labels,
        'status_values': status_values,
    }
    return render(request, 'dashboard/index.html', context)


@staff_member_required
def orders_list(request):
    orders = Order.objects.all().order_by('-created_at')
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    payment = request.GET.get('payment', '')

    if q:
        orders = orders.filter(
            Q(order_number__icontains=q) |
            Q(shipping_name__icontains=q) |
            Q(shipping_phone__icontains=q) |
            Q(user__email__icontains=q)
        )
    if status:
        orders = orders.filter(status=status)
    if payment:
        orders = orders.filter(payment_method=payment)

    context = {
        'orders': orders,
        'query': q,
        'selected_status': status,
        'selected_payment': payment,
        'status_choices': Order.STATUS_CHOICES,
        'payment_choices': Order.PAYMENT_METHOD_CHOICES,
    }
    return render(request, 'dashboard/orders.html', context)


@staff_member_required
def order_detail_staff(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order, 'status_choices': Order.STATUS_CHOICES})


@staff_member_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            old_status_name = order.get_status_display()
            order.status = new_status
            order.save()
            
            # Trigger Dual Email & In-App Notification
            try:
                from core.email_utils import notify_order_status_change
                notify_order_status_change(order, new_status)
            except Exception as e:
                print(f"Order status notification error: {e}")

            ActivityLog.objects.create(
                user=request.user,
                action=f"Updated Order #{order.order_number} status",
                details=f"Changed status from {old_status_name} to {order.get_status_display()}"
            )
            messages.success(request, f'Updated Order #{order.order_number} status to "{order.get_status_display()}".')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:orders'))


@staff_member_required
def products_list(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    q = request.GET.get('q', '').strip()
    cat = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    stock_status = request.GET.get('stock', '')

    if q:
        products = products.filter(Q(name__icontains=q) | Q(slug__icontains=q))
    if cat:
        products = products.filter(category__slug=cat)
    if brand:
        products = products.filter(brand__slug=brand)
    if stock_status == 'out':
        products = products.filter(stock=0)
    elif stock_status == 'low':
        products = products.filter(stock__gt=0, stock__lte=5)
    elif stock_status == 'in':
        products = products.filter(stock__gt=5)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'query': q,
        'selected_category': cat,
        'selected_brand': brand,
        'selected_stock': stock_status,
    }
    return render(request, 'dashboard/products.html', context)


@staff_member_required
def product_add(request):
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        brand_id = request.POST.get('brand_id')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price') or None
        stock = request.POST.get('stock', 10)
        description = request.POST.get('description', '')
        badge = request.POST.get('badge') or None

        category = get_object_or_404(Category, id=category_id)
        brand = Brand.objects.filter(id=brand_id).first() if brand_id else None

        product = Product.objects.create(
            name=name,
            category=category,
            brand=brand,
            price=price,
            discount_price=discount_price,
            stock=stock,
            description=description,
            badge=badge,
            is_available=True,
            is_featured=True
        )

        if 'main_image' in request.FILES:
            product.main_image = request.FILES['main_image']
            product.save()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Added new product: {product.name}",
            details=f"Price: ₹{product.price}, Stock: {product.stock}"
        )

        messages.success(request, f'Product "{product.name}" created successfully!')
        return redirect('dashboard:products')

    return render(request, 'dashboard/product_add.html', {'categories': categories, 'brands': brands})


@staff_member_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    p_name = product.name
    product.delete()
    messages.info(request, f'Product "{p_name}" has been deleted.')
    return redirect('dashboard:products')


@staff_member_required
def inventory_view(request):
    products = Product.objects.all().order_by('stock')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('stock')
        product = get_object_or_404(Product, id=product_id)
        old_stock = product.stock
        product.stock = int(new_stock)
        product.save()

        ActivityLog.objects.create(
            user=request.user,
            action=f"Updated inventory stock for {product.name}",
            details=f"Stock changed from {old_stock} to {product.stock}"
        )
        messages.success(request, f'Updated stock for "{product.name}" to {product.stock} units.')
        return redirect('dashboard:inventory')

    context = {
        'products': products,
        'out_of_stock': products.filter(stock=0),
        'low_stock': products.filter(stock__gt=0, stock__lte=5),
        'in_stock': products.filter(stock__gt=5),
    }
    return render(request, 'dashboard/inventory.html', context)


@staff_member_required
def customers_list(request):
    customers = User.objects.annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total_amount')
    ).order_by('-created_at')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '').strip()

        if email and password:
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Customer with email {email} already exists!')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True,
                    is_email_verified=True
                )
                messages.success(request, f'Customer account for "{user.email}" created successfully!')
                return redirect('dashboard:customers')

    return render(request, 'dashboard/customers.html', {'customers': customers})


@staff_member_required
def toggle_user_status(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if u.is_superuser:
        messages.error(request, 'Superuser account status cannot be modified!')
    else:
        u.is_active = not u.is_active
        u.save()
        status_label = "Active (Unblocked)" if u.is_active else "Blocked"
        messages.success(request, f'User account {u.email} is now {status_label}.')
    return redirect('dashboard:customers')


@staff_member_required
def customer_delete(request, user_id):
    u = get_object_or_404(User, id=user_id)
    if u.is_superuser:
        messages.error(request, 'Superuser accounts cannot be deleted!')
    else:
        email = u.email
        u.delete()
        messages.info(request, f'Customer account "{email}" deleted.')
    return redirect('dashboard:customers')


@staff_member_required
def categories_list(request):
    categories = Category.objects.annotate(product_count=Count('products')).order_by('order')

    if request.method == 'POST':
        name = request.POST.get('name')
        icon = request.POST.get('icon', 'fas fa-box')
        if name:
            cat = Category.objects.create(name=name, icon=icon, is_active=True)
            messages.success(request, f'Category "{cat.name}" created successfully!')
            return redirect('dashboard:categories')

    return render(request, 'dashboard/categories.html', {'categories': categories})


@staff_member_required
def category_delete(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    c_name = cat.name
    cat.delete()
    messages.info(request, f'Category "{c_name}" deleted.')
    return redirect('dashboard:categories')


@staff_member_required
def brands_list(request):
    brands = Brand.objects.annotate(product_count=Count('products')).order_by('name')

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            brand = Brand.objects.create(name=name, is_active=True)
            messages.success(request, f'Brand "{brand.name}" created successfully!')
            return redirect('dashboard:brands')

    return render(request, 'dashboard/brands.html', {'brands': brands})


@staff_member_required
def brand_delete(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    b_name = brand.name
    brand.delete()
    messages.info(request, f'Brand "{b_name}" deleted.')
    return redirect('dashboard:brands')


@staff_member_required
def reviews_list(request):
    reviews = Review.objects.all().select_related('product', 'user')
    return render(request, 'dashboard/reviews.html', {'reviews': reviews})


@staff_member_required
def toggle_review_status(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = not review.is_approved
    review.save()
    status_label = "Approved" if review.is_approved else "Hidden"
    messages.success(request, f'Review for "{review.product.name}" by {review.user.email} marked as {status_label}.')
    return redirect('dashboard:reviews')


@staff_member_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    messages.info(request, 'Review deleted successfully.')
    return redirect('dashboard:reviews')


@staff_member_required
def coupons_list(request):
    coupons = Coupon.objects.all()

    if request.method == 'POST':
        code = request.POST.get('code', '').upper().strip()
        discount = request.POST.get('discount')
        min_order = request.POST.get('min_order', 999)
        max_discount = request.POST.get('max_discount', 500)
        valid_to = request.POST.get('valid_to', '').strip()
        usage_limit = request.POST.get('usage_limit', 0)

        if not code:
            messages.error(request, 'Please provide a valid coupon code.')
            return redirect('dashboard:coupons')

        # Prevent duplicate code crash (UNIQUE constraint)
        if Coupon.objects.filter(code__iexact=code).exists():
            messages.error(request, f'Coupon code "{code}" already exists! Please choose a unique code.')
            return redirect('dashboard:coupons')

        expiry_datetime = None
        if valid_to:
            try:
                from django.utils.dateparse import parse_datetime, parse_date
                from datetime import datetime, time
                parsed = parse_datetime(valid_to)
                if not parsed:
                    pdate = parse_date(valid_to)
                    if pdate:
                        parsed = timezone.make_aware(datetime.combine(pdate, time.max))
                expiry_datetime = parsed
            except Exception:
                expiry_datetime = None

        try:
            usage_limit_int = int(usage_limit) if usage_limit else 0
        except ValueError:
            usage_limit_int = 0

        coupon = Coupon.objects.create(
            code=code,
            discount_percentage=discount,
            min_order_amount=min_order,
            max_discount_amount=max_discount,
            valid_to=expiry_datetime,
            usage_limit=usage_limit_int,
            is_active=True
        )

        ActivityLog.objects.create(
            user=request.user,
            action=f"Created discount coupon '{coupon.code}'",
            details=f"{coupon.discount_percentage}% OFF on orders > ₹{coupon.min_order_amount}"
        )

        messages.success(request, f'Created promo coupon "{coupon.code}" successfully!')
        return redirect('dashboard:coupons')

    return render(request, 'dashboard/coupons.html', {'coupons': coupons})


@staff_member_required
def coupon_toggle(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.is_active = not coupon.is_active
    coupon.save()
    status_str = "activated" if coupon.is_active else "deactivated"
    messages.success(request, f'Coupon "{coupon.code}" has been {status_str}.')
    return redirect('dashboard:coupons')


@staff_member_required
def coupon_delete(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    code = coupon.code
    coupon.delete()
    ActivityLog.objects.create(
        user=request.user,
        action=f"Deleted coupon '{code}'",
        details="Coupon permanently deleted by administrator."
    )
    messages.info(request, f'Coupon "{code}" has been deleted.')
    return redirect('dashboard:coupons')



@staff_member_required
def analytics_view(request):
    total_revenue = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    sales_by_category = Category.objects.annotate(
        total_sales=Sum('products__orderitem__price')
    )

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'sales_by_category': sales_by_category,
    }
    return render(request, 'dashboard/analytics.html', context)


@staff_member_required
def export_reports(request, report_type):
    response = HttpResponse(content_type='text/csv')
    
    if report_type == 'orders':
        response['Content-Disposition'] = 'attachment; filename="spcart_orders_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Order Number', 'Customer Name', 'Phone', 'Payment Method', 'Status', 'Total Amount', 'Created At'])
        for o in Order.objects.all():
            writer.writerow([o.order_number, o.shipping_name, o.shipping_phone, o.get_payment_method_display(), o.get_status_display(), o.total_amount, o.created_at])
    
    elif report_type == 'products':
        response['Content-Disposition'] = 'attachment; filename="spcart_products_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Product Name', 'Category', 'Brand', 'Price', 'Stock', 'Status'])
        for p in Product.objects.all():
            writer.writerow([p.id, p.name, p.category.name, p.brand.name if p.brand else 'None', p.effective_price, p.stock, 'Available' if p.is_available else 'Disabled'])

    elif report_type == 'customers':
        response['Content-Disposition'] = 'attachment; filename="spcart_customers_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Username', 'Email', 'Joined Date'])
        for u in User.objects.all():
            writer.writerow([u.id, u.username, u.email, u.created_at])

    return response


@staff_member_required
def activity_log_view(request):
    logs = ActivityLog.objects.all()
    return render(request, 'dashboard/activity_log.html', {'logs': logs})
