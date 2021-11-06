from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from iso3166 import countries


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is False:
            raise ValueError("Le super utilisateur doit faire partie de l'équipe d'administration.")
        if kwargs.get("is_superuser") is False:
            raise ValueError("Le super utilisateur doit être super utilisateur.")

        return self.create_user(email=email, **kwargs)


class Shopper(AbstractUser):
    username = None
    email = models.EmailField(max_length=240, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class ShippingAddress(models.Model):
    user = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    address_1 = models.CharField(max_length=1024, help_text="Adresse de voirie et numéro de rue.")
    address_2 = models.CharField(max_length=1024, blank=True, help_text="Bâtiment, étage, lieu-dit...")
    city = models.CharField(max_length=1024)
    zip_code = models.CharField(max_length=24)
    country = models.CharField(max_length=2, choices=[(c.alpha2.lower(), c.name) for c in countries])
