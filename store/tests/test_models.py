from django.test import TestCase
from django.urls import reverse

from accounts.models import Shopper
from store.models import Product, Cart, Order


class ProductTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
                name="Sneakers Docstring",
                price=10,
                stock=10,
                description="De superbes sneakers.",
        )

    def test_product_slug_is_automatically_generated(self):
        self.assertEqual(self.product.slug, "sneakers-docstring")

    def test_product_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), reverse("store:product",
                                                                  kwargs={"slug": self.product.slug}))


class CartTest(TestCase):
    def setUp(self):
        user = Shopper.objects.create_user(
                email="test@gmail.com",
                password="123456"
        )
        product = Product.objects.create(
                name="Sneakers Docstring",
        )
        self.cart = Cart.objects.create(
                user=user,
        )
        for _ in range(5):
            order = Order.objects.create(
                    user=user,
                    product=product
            )
            self.cart.orders.add(order)
        self.cart.save()

    def test_orders_cleared_from_cart_when_cart_is_deleted(self):
        orders_pk = [order.pk for order in self.cart.orders.all()]
        self.cart.delete()
        for order_pk in orders_pk:
            order = Order.objects.get(pk=order_pk)
            self.assertIsNotNone(order.ordered_date)
            self.assertTrue(order.ordered)
