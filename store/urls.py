from django.urls import path

from store.views import index, product_detail, add_to_cart, cart, delete_cart, create_checkout_session, stripe_webhook, checkout_success, update_quantities

app_name = "store"

urlpatterns = [
    path('cart/', cart, name="cart"),
    path('cart/update_quantities/', update_quantities, name="update-quantities"),
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/create-checkout-session/', create_checkout_session, name="create-checkout-session"),
    path('cart/success/', checkout_success, name="checkout-success"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
]