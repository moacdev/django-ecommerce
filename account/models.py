from django.db.models import *
from django.contrib.auth.models import AbstractUser
from mkplace.settings import AUTH_USER_MODEL

from store.models import Order

class Shopper(AbstractUser):
    pass

class Cart(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    orders = ManyToManyField(Order)
    ordered = BooleanField(default=False)
    ordered_date = DateField(blank=True, null=True)
    def __str__(self):
        return f"Panier de {self.user}"