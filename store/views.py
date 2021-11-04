import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from shop import settings
from store.models import Product, Cart, Order

stripe.api_key = settings.STRIPE_API_KEY


def index(request):
    products = Product.objects.all()

    return render(request, 'store/index.html', context={"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/detail.html', context={"product": product})


def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                 product=product)

    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity += 1
        order.save()

    return redirect(reverse("product", kwargs={"slug": slug}))


def cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    return render(request, 'store/cart.html', context={"orders": cart.orders.all()})


@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1JrtMhJ9SXnXquYKYhwlyLE6',
                'quantity': 1,
            },
                {'price': 'price_1JruYrJ9SXnXquYKdn5bR3S9',
                 'quantity': 2}
            ],
            mode='payment',
            locale='fr',
            success_url="http://127.0.0.1:8000/",
            cancel_url="http://127.0.0.1:8000/",
    )

    return redirect(session.url)


def delete_cart(request):
    if cart := request.user.cart:
        cart.orders.all().delete()
        cart.delete()

    return redirect('index')
