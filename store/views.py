from datetime import datetime

import stripe
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Shopper
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


def create_checkout_session(request):
    cart = request.user.cart
    line_items = [{"price": order.product.stripe_id,
                   "quantity": order.quantity} for order in cart.orders.all()]

    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            locale='fr',
            success_url=request.build_absolute_uri(reverse('checkout-success')),
            cancel_url=request.build_absolute_uri(reverse('cart')),
    )

    return redirect(session.url)


def checkout_success(request):
    return render(request, 'store/success.html')


def delete_cart(request):
    if cart := request.user.cart:
        cart.orders.all().delete()
        cart.delete()

    return redirect('index')


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = "whsec_PNuis6u3LGEXaoOmo6JC8T2Twompq1iR"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        return complete_order(session=session)

    return HttpResponse(status=200)


def complete_order(session):
    try:
        user_email = session["customer_details"]["email"]
    except KeyError:
        return HttpResponse("Invalid user email", status=404)

    user = get_object_or_404(Shopper, email=user_email)
    user.cart.ordered = True
    user.cart.ordered_date = timezone.now()
    user.cart.save()
    return HttpResponse(status=200)
