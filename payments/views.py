import mercadopago
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

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
                'title': order.title,
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


def addtocart(request):
    if request.method == 'GET':
        # Destroying the session
        # if request.session.get('cart_items'):
        #     del request.session['cart_items']
        #     request.session.save()

        product_id = request.GET.get('product_id')  # Obter o ID do produto
        if not product_id:
            messages.error(request, 'This product does not exist.')
            return redirect('home')

        product = get_object_or_404(Payment, pk=product_id)

        # Obter a lista de itens no carrinho da sessão
        title = product.title
        value = float(product.value)
        quantity = 1

        if not request.session.get('cart_items'):
            request.session['cart_items'] = {}
            request.session.save()

        cart_items = request.session['cart_items']

        if product_id in cart_items:
            quantitly_cart = cart_items[product_id]['quantity']
            quantitly_cart += 1

            cart_items[product_id]['quantity'] = quantitly_cart
            cart_items[product_id]['value'] = value * quantitly_cart

        else:
            cart_items[product_id] = {
                'product_id': product_id,
                'title': title,
                'value': value,
                'quantity': quantity,
            }
        request.session.save()
        messages.success(request, 'Product added to cart.')
        return redirect('home')
