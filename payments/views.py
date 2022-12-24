import mercadopago
from django.conf import settings
from django.shortcuts import redirect, render

from .models import Payment

sdk = mercadopago.SDK(settings.ACCESS_TOKEN)

# Create your views here.


def home(request):
    if request.method == 'GET':
        products = Payment.objects.all()
        # Obter a lista de itens no carrinho da sessão
        cart_items = request.session.get('cart_items')
        context = {
            'products': products,
            'cart_items': cart_items,
        }
        return render(request, 'payments/pages/home.html', context)

    if request.method == 'POST':
        product_ids = request.session.get('cart_items')
        for product_id in product_ids:
            quantitly_cart = product_ids[product_id]['quantity']
        orders = Payment.objects.filter(pk__in=product_ids)
        # Criar um dicionário com as informações de pagamento
        payment_data = {
            'items': [],
            'payer': {
                'name': 'João da Silva',
                'email': 'joao@example.com'
            }
        }
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        payment_data['back_urls'] = {
            "success": domain + "/success/",
            "failure": domain + "/failure/",
            "pending": domain + "/pending/"
        }
        # Adicionar os produtos à lista de items
        for order in orders:
            # Obter a quantidade do item da sessão
            item = {
                'title': order.description,
                'quantity': quantitly_cart,
                'currency_id': order.currency,
                'unit_price':  float(order.value * quantitly_cart)
            }
            payment_data['items'].append(item)

    # Criar a preferência de pagamento
    preference_response = sdk.preference().create(payment_data)

    # Obter o link para o Checkout Pro
    checkout_url = preference_response['response']['init_point']
    return redirect(checkout_url)
