from django.http import HttpResponse
from django.shortcuts import render

from store.models import Categorie, Product


def homepage(request):
    return render(request, 'store/index.html', { "categories": Categorie.objects.all(), "products": Product.objects.all() })