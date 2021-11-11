from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from shop.settings import AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True)
    stripe_id = models.CharField(max_length=90, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.email or "Unknown"

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)