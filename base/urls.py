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
import json
from math import prod
from pickle import FALSE
from sqlite3 import Date
import uuid
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path
from django.core import serializers
from account.models import Address, Cart, PaymentMethod, WishList
from base.helpers import format_price, serializeCart, serializeUserOrders, serializeWishList
from store.models import Categorie, Order, Product
from store.views import categories, categoryProducts, homepage, login, product, products, register
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.conf.urls import (handler400, handler403, handler404, handler500)


def accountInfo(request):
    if request.user.id is None:
        return redirect(to="/connexion")
    tabIndex = 0
    if request.GET.get('tab'):
        tab = request.GET.get('tab')
        if tab == 'profil':
            tabIndex = 0
        elif tab == 'adresses':
            tabIndex = 1
        elif tab == 'paiement':
            tabIndex = 2
        elif tab == 'changer-mot-de-passe':
            tabIndex = 3

    user = request.user
    address = Address.objects.filter(user=user).first()
    pm = PaymentMethod.objects.filter(user=user).first()
    return render(request, "store/account.html", { "categories": Categorie.objects.all(), 'tabIndex': tabIndex, 'user': request.user, 'address': address, 'pm': pm.method })

def orderCart(request):
    if request.user.id is None:
        return redirect(to="/connexion")
    
    user = request.user
    address = Address.objects.filter(user=user).first()

    payment_method = PaymentMethod.objects.filter(user=user).first()
    cart = userCart = Cart.objects.filter(user=request.user, ordered=False)
    cart, cartSum = serializeCart(userCart)

    return render(request, "store/order-cart.html", { "categories": Categorie.objects.all(), 'user': request.user , 'address': address,'payment_method': payment_method, 'cart': cart, 'cartSum': cartSum })

def changePwd(request):
    if request.user.id is None:
        return redirect(to="/connexion")
    return render(request, "store/change-password.html", { "categories": Categorie.objects.all() })
def wishList(request):
    if request.user.id is None:
        return redirect(to="/connexion")
    wishList = WishList.objects.filter(user=request.user).first()
    return render(request, "store/wishlist.html", {'wishList': serializeWishList(wishList), "categories": Categorie.objects.all() })

def cart(request):
    if request.user.id is None:
        return redirect(to="/connexion")
    # Récupere le panier de utilisateur
    userCart = Cart.objects.filter(user=request.user, ordered=False).first()
    return render(request, "store/cart.html", { "categories": Categorie.objects.all(), 'cart': userCart })

def orders(request):
    if request.user.id is None:
        return redirect(to="/connexion")
    user = request.user
    userOrders = Order.objects.filter(user=user)
    return render(request, "store/orders.html", { "categories": Categorie.objects.all(), 'userOrders': serializeUserOrders(userOrders) })

def search(request):
    return render(request, "store/search.html", { "categories": Categorie.objects.all() })

def storeInfo(request):
    # latitude = '12.659584'
    # longitude = '-7.966160'
    # key = 'AIzaSyC7z8j8wQVsk5Q-0fL-kt3bAeV1tJkuynE'
    return render(request, "store/my-store.html", {"categories": Categorie.objects.all()})


def apiChangePassword(request):
    # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()
    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })
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
    if request.method != 'POST':
        raise PermissionDenied()
    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })
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
    # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()
    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    phone = request.POST.get('phone')

    request.user.username = username
    request.user.email = email
    request.user.phone = phone
    request.user.save()

    # On return à la vue une reponse comme quoi tous ses bien passée
    return JsonResponse({ "isOk": True })

def apiChangePaymentInfo(request):
    # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()
    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })

    method = (json.loads(request.body))['method']
    if method is None:
        return JsonResponse({ "isOk": False, "error_type": 'invalid-data' })

    user = request.user

    if PaymentMethod.objects.filter(user=user).exists() == True:
        user_method = PaymentMethod.objects.filter(user=user).first()
        user_method.method = method
        user_method.save()
    else:
        PaymentMethod.objects.create(user=user, method=method)

    # On return à la vue une reponse comme quoi tous ses bien passée
    return JsonResponse({ "isOk": True })

def apiGetCart(request):
     # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()
    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })
    print(request.user.id == None)
    # Récupere le panier de utilisateur
    userCart = Cart.objects.filter(user=request.user, ordered=False)
    cart, cartSum = serializeCart(userCart)
    
    cartCount = Cart.objects.filter(user=request.user, ordered=False).count()
    # On return la reponse a la vue
    return JsonResponse({ "isOk": True, 'cart': cart, 'cartCount':cartCount, 'cartSum': format_price(str(cartSum))  })

def apiAddToCart(request):
     # On accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()
    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })

    productID = (json.loads(request.body))['productID']
    qty = 1
    if 'qty' in str(request.body):
        qty = (json.loads(request.body)).get('qty')
    if productID is None:
        return JsonResponse({ "isOk": False })

    user = request.user

    # Recuperation du produit
    product = Product.objects.filter(pk=productID).first()
    if product is None:
        return JsonResponse({ "isOk": False, 'error_type': "product-not-exist" })

    # Verifie si l'utilisateur n'a pas déjà le produit dans son panier
    isUserHasInCart = Cart.objects.filter(user=user, product=product, ordered=False).first()
    if isUserHasInCart:
        return JsonResponse({ "isOk": False, 'error_type': "product-in-cart" })
        
    # on le cree
    Cart.objects.create(user=user, product=product, quantity=qty)
    cartCount = Cart.objects.filter(user=user, ordered=False).count()
    
    
    # On return la reponse a la vue
    return JsonResponse({ "isOk": True, 'cartCount': cartCount  })

# fonction api permettant d'ajouter un favoris/souhait
def apiAddToFav(request):

     # On n'accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()

    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })


    productID = (json.loads(request.body))['productID']

    if productID is None:
        return JsonResponse({ "isOk": False })

    user = request.user

    # Recuperation du produit
    product = Product.objects.filter(pk=productID).first()
    if product is None:
        return JsonResponse({ "isOk": False, 'error_type': "product-not-exist" })

    # Verifie si l'utilisateur n'a pas déjà le produit dans ses favoris
    userWishList = WishList.objects.filter(user=user).first()
    if userWishList:

        if userWishList.product.filter(id=productID):
            return JsonResponse({ "isOk": False, 'error_type': "product-in-fav" })
        userWishList.product.add(product)
    else:
        # on le cree
        userWishList = WishList.objects.create(user=user)
        userWishList.product.add(product)
    
    
    # On return la reponse a la vue
    return JsonResponse({ "isOk": True, 'wishCount': userWishList.product.count()  })

def ApiOrderCart(request):

     # On n'accepte que les requêtes en postes et l'utilisateur doit aussi être authentifié authentifié
    if request.method != 'POST':
        raise PermissionDenied()

    # Si l'utilisateur n'est pas connecter o arrete
    if request.user.id is None:
        return JsonResponse({ "isOk": False, "error_type": 'not-logged' })

    user = request.user

    if user.phone is None or user.phone == '':
        return JsonResponse({ "isOk": False, "error_type": 'empty-phone' })

    address = Address.objects.filter(user=user).exists()
    
    if address == False:
        return JsonResponse({ "isOk": False, "error_type": 'empty-address' })

    paymentMethod = PaymentMethod.objects.filter(user=user).exists()

    if paymentMethod == False:
        return JsonResponse({ "isOk": False, "error_type": 'empty-payment-method' })

    if Cart.objects.filter(user=user, ordered=False).exists() == False:
        return JsonResponse({ "isOk": False, "error_type": 'empty-cart' })

    userActivesCart = Cart.objects.filter(user=user, ordered=False)

    applyCartOrdered = Order.objects.create(user=user)

    for cart in userActivesCart:
        cart.ordered = True
        cart_product = Product.objects.filter(pk=cart.product.id).first()
        cart_product.sold_count += 1
        cart.ordered_date = Date.today()
        cart.save()
        applyCartOrdered.cart.add(cart)
    
    # On return la reponse a la vue
    return JsonResponse({ "isOk": True })



urlpatterns = [
    path('', homepage),
    path('connexion/', login),
    path('inscription/', register),
    path('categories/', categories),
    path('produits/', products),
    path('categories/<str:category>', categoryProducts),
    path('categories/<str:category>/<str:product>', product),


    path('mon-compte/', accountInfo),
    path('liste-de-souhait', wishList),
    path('mes-commandes', orders),
    path('recherche/', search),
    path('boutique/', storeInfo),

    path('commander-mon-panier/', orderCart),
    path('api/order-cart/', ApiOrderCart),

    path('api/account/change-password', apiChangePassword),
    path('api/account/change-addresses-info', apiChangeAddresses),
    path('api/account/change-profil-info', apiChangeProfilInfo),
    path('api/account/change-payment-info', apiChangePaymentInfo),
    path('api/get-cart', apiGetCart),
    path('api/add-to-cart', apiAddToCart),
    path('api/add-to-fav', apiAddToFav),



    path('admin/', admin.site.urls),
]

handler404 = 'store.views.handler404'
handler403 = 'store.views.handler403'
handler500 = 'store.views.handler500'