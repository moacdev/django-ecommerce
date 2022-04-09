from django.db.models import *
from django.contrib.auth.models import AbstractUser
from base.settings import AUTH_USER_MODEL

from store.models import Order



class Shopper(AbstractUser):
    phone = CharField(unique=True, null=True, max_length=15)
    email = EmailField('Adresse email', unique=True)
    def __str__(self) -> str:
        return super().username

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
    ordered = BooleanField(blank=True, null=True, default=False)
    quantity = IntegerField(default=1)
    ordered_date = DateField(blank=True, null=True)
    def __str__(self):
        return f"{self.product} au panier de {self.user}"

class WishList(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    product = ManyToManyField('store.Product')
    def __str__(self):
        return f"{self.product} favoris de {self.user}"

class PaymentMethodTypes(Model):
    method = CharField('Methode de paiement', max_length=100)
    def __str__(self):
        return f"Paiment par {self.method}"

class PaymentMethod(Model):
    user = OneToOneField(AUTH_USER_MODEL, on_delete=CASCADE)
    method = CharField('Methode de paiement', max_length=100) # ForeignKey(PaymentMethodTypes, on_delete=CASCADE)
    def __str__(self):
        return f"{self.method} de {self.user}"


