import math
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.template import RequestContext
from account.models import Shopper
from base.helpers import format_price, serializeProducts
from store.models import Categorie, Product
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def homepage(request):
    products = Product.objects.all()
    for _product in products:
        _product.price = format_price(str(_product.price))
            
        
    return render(request, 'store/index.html', { "categories": Categorie.objects.all(), "products": products })

def login(request):
    if request.user.id != None:
        redirect('/')
    if request.method == "POST":
        if request.POST.get("login") != "" and request.POST.get("password") != "":
            login = request.POST.get("login")
            password = request.POST.get("password")
            user = authenticate(request, username=login, password=password)
            if user is not None:
                return redirect("/")
            else:
                return render(request, "store/login.html", { "error": "Identifiants ou mot de passe incorrecte", "email": request.POST.get("email") })
        else:
            return render(request, "store/login.html", { "error": "Identifiants incorrecte", "email": request.POST.get("email") })
    return render(request, "store/login.html", {"email": ""})

def register(request):
    if request.user.id != None:
        redirect('/')
    if request.method == "POST":
        if request.POST.get("email") != "" and request.POST.get("username") != "" and request.POST.get("phone") != "" and request.POST.get("password") != "" and request.POST.get("password_confirmation") != "":
            try:
                validate_email(request.POST.get("email"))
            except ValidationError:
                return render(request, "store/register.html", { "error": "Format d'email incorrecte", "email": request.POST.get("email") })
            if request.POST.get("password") != request.POST.get("password_confirmation"):
                return render(request, "store/register.html", { "error": "Les 2 mot de passes ne correspondes pas !", "email": request.POST.get("email") })
            email = request.POST.get("email")
            username = request.POST.get("username")
            phone = request.POST.get("phone")
            password = request.POST.get("password")
            user = Shopper.objects.create_user(username, email, password)
            user.phone = phone
            user.save()
            return redirect("/connexion")
        else: return render(request, "store/register.html", { "error": "Renseignez tous les champs !", "email": request.POST.get("email") })
    return render(request, "store/register.html",{ "categories": Categorie.objects.all() })

def logout_view(request):
    logout(request)

def categories(request):
    
    categories = Categorie.objects.all()
    return render(request, "store/categories.html", { "categories": Categorie.objects.all() })

def products(request):
    categories = Categorie.objects.all()
    if  request.GET.get('categorie'):
        category = get_object_or_404(Categorie, slug=request.GET.get('categorie'))
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
        productCount = products.count()

    currentPage = 1
    if request.GET.get('page'):
        currentPage = int(request.GET.get('page'))
    
    productPerPage = 3
    pages = math.ceil(productCount / productPerPage)

    
    pageOffset = 2
    currentPagePrvOffset = int(math.fabs(currentPage - pageOffset ))
    if currentPagePrvOffset < 1:
        currentPagePrvOffset = 1
    lastPagePrvOffset = int(math.fabs(pages - pageOffset ))
    if currentPagePrvOffset > pages:
        currentPagePrvOffset = pages
    pageOffsetBtw = pageOffset * 2

    take_from = productPerPage * (currentPage-1)

    

    pagination = {
        'pages' : pages,
        'productPerPage' : productPerPage,
        'currentPage': currentPage,
        'pageOffset': pageOffset,
        'pageOffsetBtw': pageOffsetBtw,
        'currentPagePrvOffset': currentPagePrvOffset,
        'lastPagePrvOffset': lastPagePrvOffset,
        'currentPagePrvOffsetToPageOffset': list(range(currentPagePrvOffset, pageOffset+1)),
        'lastPagePrvOffsetToPageCount': list(range(lastPagePrvOffset, pages+1)),
        'currentPagePrvOffsetToPagesCount': list(range(currentPagePrvOffset, pages+1)),
    }

    print(pagination['currentPagePrvOffsetToPagesCount'])


    return render(request, "store/products.html", {'pagination': pagination, 'productCount': productCount, "categories": Categorie.objects.all(), 'products': serializeProducts(products)[take_from:take_from+productPerPage] })

def category(request, category):
    _category = get_object_or_404(Categorie, slug=category)
    return render(request, "store/category.html", { "categories": Categorie.objects.all(), "category": _category, "products": Product.objects.filter(category=_category.id) })

def product(request, category, product):
    _category = get_object_or_404(Categorie, slug=category)
    _product = get_object_or_404(Product, slug=product, category=_category.id)
    return render(request, "store/view_product.html", { "categories": Categorie.objects.all(), "category": _category, "product": _product })


def handler404(request, exception):
    response = render("404.html")
    response.status_code = 404
    return response

def handler403(request, exception):
    response = render("403.html")
    response.status_code = 403
    return response

def handler500(request):
    response = render("500.html")
    response.status_code = 500
    return response
