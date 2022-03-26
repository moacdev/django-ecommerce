"""base URL Configuration

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
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from account.models import Address
from store.models import Categorie, Product
from store.views import categories, category, homepage, login, product, register
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def accountInfo(request):
    if request.user.is_authenticated != True:
        return redirect(to="/connexion")
    
    user = request.user
    address = Address.objects.get(user=user)

    print(address)

    return render(request, "store/account.html", { "categories": Categorie.objects.all(), 'user': request.user, 'address': address })
def changePwd(request):
    if request.user.is_authenticated != True:
        return redirect(to="/connexion")
    return render(request, "store/change-password.html", { "categories": Categorie.objects.all() })
def wishList(request):
    if request.user.is_authenticated != True:
        return redirect(to="/connexion")
    return render(request, "store/wishlist.html", { "categories": Categorie.objects.all() })

def cart(request):
    if request.user.is_authenticated != True:
        return redirect(to="/connexion")
    return render(request, "store/cart.html", { "categories": Categorie.objects.all() })
def orders(request):
    if request.user.is_authenticated != True:
        return redirect(to="/connexion")
    return render(request, "store/orders.html", { "categories": Categorie.objects.all() })
def search(request):
    return render(request, "store/search.html", { "categories": Categorie.objects.all() })
def helpFAQ(request):
    return render(request, "store/faq.html", { "categories": Categorie.objects.all() })


def apiChangePassword(request):
    # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST' and request.user.is_authenticated != True:
        raise PermissionDenied()
    # On récupere les donnée envoyée
    current_password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    password_confirm = request.POST.get('password_confirmation')
    # On vérifie si les donnée sont valide
    if not current_password or not new_password or not password_confirm or (new_password != password_confirm):
        return JsonResponse({ "isOk": False,  "error_type": "fields-invalid"  })
    # On vérifie si le mot de pass actuelle est valide
    if not request.user.check_password(current_password):
            return JsonResponse({ "isOk": False,  "error_type": "password-invalid"  })
    # On met à jour le mot de passe du user
    request.user.set_password(new_password)
    request.user.save()
    # On return à la vue une reponse comme quoi tous ses bien passée
    return JsonResponse({ "isOk": True })


def apiChangeAddresses(request):
    # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST' and request.user.is_authenticated != True:
        raise PermissionDenied()
    # On récupere les donnée envoyée
    country = request.POST.get('country')
    city = request.POST.get('city')
    common = request.POST.get('common')
    quarter = request.POST.get('quarter')
    streetDoor = request.POST.get('streetDoor')
    zipcode = request.POST.get('zipcode')
    user = request.user
    try:
        Address.objects.update_or_create(user=user, defaults={"country":country, "city":city, "common":common, "quarter":quarter, "street_door":streetDoor, "zipcode":zipcode, "user": user} )
    except:
        return JsonResponse({ "isOk": False })

    # On return à la vue une reponse comme quoi tous ses bien passée
    return JsonResponse({ "isOk": True })

def apiChangeProfilInfo(request):
    return render(request, "store/faq.html", { "categories": Categorie.objects.all() })
def apiChangePaymentInfo(request):
    return render(request, "store/faq.html", { "categories": Categorie.objects.all() })


urlpatterns = [
    path('', homepage),
    path('connexion/', login),
    path('inscription/', register),
    path('categories/', categories),
    path('categories/<str:category>', category),
    path('categories/<str:category>/<str:product>', product),


    path('mon-compte/', accountInfo),
    path('liste-de-souhaits', wishList),
    path('mon-panier', cart),
    path('mes-commandes', orders),
    path('recherche/', search),
    path('faq/', helpFAQ),

    path('api/account/change-password', apiChangePassword),
    path('api/account/change-addresses-info', apiChangeAddresses),
    path('api/account/change-profil-info', apiChangeProfilInfo),
    path('api/account/change-payment-info', apiChangePaymentInfo),



    path('admin/', admin.site.urls),
]
