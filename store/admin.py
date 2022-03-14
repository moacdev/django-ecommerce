from django.contrib import admin

from store.models import Categorie, Order, Product

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Categorie)