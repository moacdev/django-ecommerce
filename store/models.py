import datetime
from uuid import uuid4
from django.db.models import *

from base.settings import AUTH_USER_MODEL

class Categorie(Model):
    label = CharField(max_length=128, blank=True)
    slug = SlugField(max_length=128, blank=True)
    image = ImageField(upload_to="static/images", blank=True)
    def __str__(self):
        return f"{self.label}"

class Product(Model):
    label = CharField(max_length=128, blank=True)
    slug = SlugField(max_length=128, blank=True)
    description = TextField(blank=True)
    price = IntegerField(default=0)
    stock = IntegerField(default=0)
    category = ForeignKey(Categorie, on_delete=CASCADE, blank=True)
    image1 = ImageField(upload_to="static/images")
    image2 = ImageField(upload_to="static/images", blank=True)
    image3 = ImageField(upload_to="static/images", blank=True)
    image4 = ImageField(upload_to="static/images", blank=True)

    def __str__(self):
        return f"{self.label} stock: {self.stock}"

class Order(Model):
    user = ForeignKey(AUTH_USER_MODEL, on_delete=CASCADE)
    code = UUIDField(default = uuid4, editable = False)
    cart = ManyToManyField('account.Cart')
    ordered_date = DateField(default=datetime.date.today)
    finished = BooleanField(default=False)
    finished_date = DateField(blank=True, null=True)

    def __str__(self):
        return f"Nouvelle commande de {self.user} {self.ordered_date}"