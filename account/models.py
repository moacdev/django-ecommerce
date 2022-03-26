from django.db.models import *
from django.contrib.auth.models import AbstractUser
from base.settings import AUTH_USER_MODEL

from store.models import Order



class Shopper(AbstractUser):
    phone = CharField(unique=True, null=True, max_length=15)
    def __str__(self) -> str:
        return super().username

class Address(Model):
    country = CharField('Pays', max_length=128, default="Mali", blank=True)
    city = CharField('Ville', max_length=128, blank=True)
    common = CharField('Commune', max_length=128, blank=True)
    quarter = CharField('Quartier', max_length=128, blank=True)
    street_door = CharField('Rue et porte', max_length=128, blank=True)
    zipcode = CharField('Code postal', max_length=128, blank=True)
    user = OneToOneField(AUTH_USER_MODEL, on_delete=CASCADE)
    def __str__(self) -> str:
        return f"Adresse de {self.user}"

class Cart(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    orders = ManyToManyField(Order)
    ordered = BooleanField(default=False)
    ordered_date = DateField(blank=True, null=True)
    def __str__(self):
        return f"Panier de {self.user}"