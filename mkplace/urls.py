"""mkplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path
from store.models import Categorie, Product
from store.views import homepage

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

urlpatterns = [
    path('', homepage),
    path('connexion/', login),
    path('inscription/', register),
    path('categories/', categories),
    path('categories/<str:category>', category),
    path('categories/<str:category>/<str:product>', product),
    path('admin/', admin.site.urls),
]
