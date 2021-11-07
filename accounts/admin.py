from django.contrib import admin

from accounts.models import Shopper, ShippingAddress

admin.site.register(Shopper)
admin.site.register(ShippingAddress)
