from django.db.models import *
from django.contrib.auth.models import AbstractUser
from base.settings import AUTH_USER_MODEL
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Shopper(AbstractUser):
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_vendor = BooleanField(default=True)
    def __str__(self) -> str:
        return super().username

class Store(Model):
    owner = OneToOneField(Shopper, on_delete=CASCADE, related_name='store')
    name = CharField(max_length=100)
    description = TextField(blank=True)
    email = EmailField()
    def __str__(self):
        return self.name

class Address(Model):
    country = CharField('Pays', max_length=128, default="Mali", blank=True)
    city = CharField('Ville', max_length=128, blank=True)
    common = CharField('Commune', max_length=128, blank=True)
    quarter = CharField('Quartier', max_length=128, blank=True)
    street_door = CharField('Rue et porte', max_length=128, blank=True)
    zipcode = CharField('Code postal', max_length=128, blank=True)
    loc = CharField('GPS', max_length=128, blank=True)
    user = OneToOneField(AUTH_USER_MODEL, on_delete=CASCADE)
    def __str__(self) -> str:
        return f"Adresse de {self.user}"

class Cart(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    product = ForeignKey('store.Product', on_delete=CASCADE)
    vendor = ForeignKey('store.Vendor', on_delete=CASCADE)
    ordered = BooleanField(blank=True, null=True, default=False)
    quantity = IntegerField(default=1)
    ordered_date = DateField(blank=True, null=True)
    def __str__(self):
        return f"{self.product} au panier de {self.user}"

class WishList(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    product = ManyToManyField('store.Product')
    vendors = ManyToManyField('store.Vendor')
    def __str__(self):
        return f"favoris de {self.user}"

class PaymentMethodTypes(Model):
    method = CharField('Methode de paiement', max_length=100)
    def __str__(self):
        return f"Paiment par {self.method}"

class PaymentMethod(Model):
    user = OneToOneField(AUTH_USER_MODEL, on_delete=CASCADE)
    method = CharField('Methode de paiement', max_length=100)
    def __str__(self):
        return f"{self.method} de {self.user}"

