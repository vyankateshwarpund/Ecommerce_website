from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_cart')
        if not cart:
            cart = self.session['session_cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.effective_price),
                'mrp': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)
        
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        # Clean up any key where product was deleted from DB
        for pid in list(self.cart.keys()):
            if pid not in product_map:
                continue
            p = product_map[pid]
            item = self.cart[pid]
            yield {
                'product': p,
                'quantity': int(item['quantity']),
                'price': Decimal(str(item['price'])),
                'mrp': Decimal(str(item['mrp'])),
                'total_price': Decimal(str(item['price'])) * int(item['quantity']),
                'total_mrp': Decimal(str(item['mrp'])) * int(item['quantity']),
            }

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(str(item['price'])) * int(item['quantity']) for item in self.cart.values())

    def get_total_mrp(self):
        return sum(Decimal(str(item['mrp'])) * int(item['quantity']) for item in self.cart.values())

    def get_total_savings(self):
        return self.get_total_mrp() - self.get_total_price()

    def clear(self):
        if 'session_cart' in self.session:
            del self.session['session_cart']
            self.save()
