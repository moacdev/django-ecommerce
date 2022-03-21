from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from account.models import Shopper
from store.models import Categorie, Product
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def homepage(request):
    return render(request, 'store/index.html', { "categories": Categorie.objects.all(), "products": Product.objects.all() })

def login(request):
    if request.user.is_authenticated == True:
        redirect('/')
    if request.method == "POST":
        if request.POST.get("email") != "" and request.POST.get("password") != "":
            try:
                validate_email(request.POST.get("email"))
            except ValidationError:
                return render(request, "store/login.html", { "error": "Email incorrecte", "email": request.POST.get("email") })
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                return redirect("/")
            else:
                return render(request, "store/login.html", { "error": "Email ou mot de passe incorrecte", "email": request.POST.get("email") })
    return render(request, "store/login.html", {"email": ""})

def register(request):
    if request.user.is_authenticated == True:
        redirect('/')
    if request.method == "POST":
        if request.POST.get("email") != "" and request.POST.get("password") != "" and request.POST.get("password_confirmation") != "":
            try:
                validate_email(request.POST.get("email"))
            except ValidationError:
                return render(request, "store/register.html", { "error": "Format d'email incorrecte", "email": request.POST.get("email") })
            if request.POST.get("password") != request.POST.get("password_confirmation"):
                return render(request, "store/register.html", { "error": "Les 2 mot de passes ne correspondes pas !", "email": request.POST.get("email") })
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = Shopper.objects.create_user("aaaaa", email, password)
            user.username = "aab"
            user.save()
            return redirect("/connexion")
    return render(request, "store/register.html",{ "categories": Categorie.objects.all() })

def logout_view(request):
    logout(request)

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
