import datetime
from uuid import uuid4
from django.db.models import *
from django.utils.text import slugify

from base.settings import AUTH_USER_MODEL

class Categorie(Model):
    label = CharField(max_length=128, blank=True)
    slug = SlugField(max_length=128, blank=True, unique=True)
    image = ImageField(upload_to="static/images", blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        super(self).save(*args, **kwargs)
    def __str__(self):
        return f"{self.label}"

class Product(Model):
    label = CharField(max_length=128, blank=True)
    slug = SlugField(max_length=128, blank=True, unique=True)
    description = TextField(blank=True)
    price = IntegerField('prix',default=0)
    stock = IntegerField(default=0)
    sold_count = IntegerField('Nombre de ventes',default=0)
    view_count = IntegerField('Nombre de vues',default=0)
    category = ForeignKey(Categorie, on_delete=CASCADE, blank=True)
    image1 = ImageField(upload_to="static/images")
    image2 = ImageField(upload_to="static/images", blank=True)
    image3 = ImageField(upload_to="static/images", blank=True)
    image4 = ImageField(upload_to="static/images", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.label)
        super(self).save(*args, **kwargs)

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