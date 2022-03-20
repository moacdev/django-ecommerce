from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from store.models import Categorie, Product


def homepage(request):
    return render(request, 'store/index.html', { "categories": Categorie.objects.all(), "products": Product.objects.all() })

def login(request):
    return render(request, "store/login.html",{ "categories": Categorie.objects.all() })

def register(request):
    return render(request, "store/register.html",{ "categories": Categorie.objects.all() })

def categories(request):
    categories = Categorie.objects.all()
    return render(request, "store/categories.html", { "categories": Categorie.objects.all() })

def category(request, category):
    _category = get_object_or_404(Categorie, slug=category)
    return render(request, "store/category.html", { "categories": Categorie.objects.all(), "category": _category, "products": Product.objects.filter(category=_category.id) })

def product(request, category, product):
    print(category)
    _category = get_object_or_404(Categorie, slug=category)
    _product = get_object_or_404(Product, slug=product, category=_category.id)
    return render(request, "store/view_product.html", { "categories": Categorie.objects.all(), "category": _category, "product": _product })
