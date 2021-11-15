from django.test import TestCase
from django.urls import reverse

from accounts.models import Shopper
from store.models import Product


class StoreTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
                name="Sneakers Docstring",
                price=10,
                stock=10,
                description="De superbes sneakers.",
        )

    def test_products_are_shown_on_index_page(self):
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.product.name, str(resp.content))

    def test_connexion_link_when_user_not_connected(self):
        resp = self.client.get(reverse("index"))
        self.assertIn("Connexion", str(resp.content))

    def test_redirect_when_anonymous_user_access_cart_view(self):
        resp = self.client.get(reverse('store:cart'))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, f"{reverse('accounts:login')}?next={reverse('store:cart')}", status_code=302)


class StoreLoggedInTest(TestCase):
    def setUp(self):
        self.user = Shopper.objects.create_user(
                email="patrick@gmail.com",
                first_name="Patrick",
                last_name="Smith",
                password="123456789"
        )

    def test_valid_login(self):
        data = {'email': 'patrick@gmail.com', 'password': '123456789'}
        resp = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(reverse('index'))
        self.assertIn("Mon profil", str(resp.content))

    def test_invalid_login(self):
        data = {'email': 'patrick@gmail.com', 'password': '1234'}
        resp = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "accounts/login.html")

    def test_profile_change(self):
        self.client.login(email="patrick@gmail.com", password="123456789")
        data = {'email': 'patrick@gmail.com',
                'password': '123456789',
                'first_name': 'Patrick',
                'last_name': 'Martin'}
        resp = self.client.post(reverse('accounts:profile'), data=data)
        self.assertEqual(resp.status_code, 302)
        patrick = Shopper.objects.get(email="patrick@gmail.com")
        self.assertEqual(patrick.last_name, "Martin")
