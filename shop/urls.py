from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from store.views import index, product_detail, add_to_cart, cart, delete_cart, create_checkout_session, stripe_webhook, checkout_success
from accounts.views import signup, logout_user, login_user

from shop import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name="signup"),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name="logout"),
    path('cart/', cart, name="cart"),
    path('stripe-webhook/', stripe_webhook, name="stripe-webhook"),
    path('cart/create-checkout-session/', create_checkout_session, name="create-checkout-session"),
    path('cart/success/', checkout_success, name="checkout-success"),
    path('cart/delete/', delete_cart, name="delete-cart"),
    path('product/<str:slug>/', product_detail, name="product"),
    path('product/<str:slug>/add-to-cart/', add_to_cart, name="add-to-cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
