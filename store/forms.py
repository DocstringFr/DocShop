from django import forms

from store.models import Order


class OrderForm(forms.ModelForm):
    quantity = forms.ChoiceField(choices=[(i, i) for i in range(1, 11)])
    delete = forms.BooleanField(initial=False,
                                required=False,
                                label="Supprimer")

    class Meta:
        model = Order
        fields = ["quantity"]

    def save(self, *args, **kwargs):
        if self.cleaned_data["delete"]:
            self.instance.delete()
            if self.instance.user.cart.orders.count() == 0:
                self.instance.user.cart.delete()
            return True

        return super().save(*args, **kwargs)
