from django.test import TestCase

from accounts.models import Shopper
from store.models import Product


class UserTest(TestCase):
    def setUp(self):
        Product.objects.create(
                name="Sneakers Docstring",
                price=10,
                stock=10,
                description="De superbes sneakers.",
        )
        self.user = Shopper.objects.create_user(
                email="test@gmail.com",
                password="123456"
        )

    def test_add_to_cart(self):
        self.user.add_to_cart(slug="sneakers-docstring")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().product.slug, "sneakers-docstring")
        self.user.add_to_cart(slug="sneakers-docstring")
        self.assertEqual(self.user.cart.orders.count(), 1)
        self.assertEqual(self.user.cart.orders.first().quantity, 2)
