from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
import json
from sqlite3 import Date

from .models import Address, Cart, PaymentMethod, WishList
from store.models import Product, Categorie, Order, Store, Shopper, Vendor
from base.helpers import format_price, serializeCart, serializeUserOrders, serializeWishList

@login_required
def account_info(request):
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
    return render(request, "store/account.html", {
        "categories": Categorie.objects.all(),
        'tabIndex': tabIndex,
        'user': request.user,
        'address': address,
        'pm': pm.method if pm else None
    })

@login_required
def order_cart(request):
    user = request.user
    address = Address.objects.filter(user=user).first()
    payment_method = PaymentMethod.objects.filter(user=user).first()
    cart = Cart.objects.filter(user=request.user, ordered=False)
    cart, cartSum = serializeCart(cart)

    return render(request, "store/order-cart.html", {
        "categories": Categorie.objects.all(),
        'user': request.user,
        'address': address,
        'payment_method': payment_method,
        'cart': cart,
        'cartSum': cartSum
    })

@login_required
def wish_list(request):
    wishList = WishList.objects.filter(user=request.user).first()
    return render(request, "store/wishlist.html", {
        'wishList': serializeWishList(wishList),
        "categories": Categorie.objects.all()
    })

@login_required
def cart_view(request):
    userCart = Cart.objects.filter(user=request.user, ordered=False).first()
    return render(request, "store/cart.html", {
        "categories": Categorie.objects.all(),
        'cart': userCart
    })

@login_required
def orders(request):
    userOrders = Order.objects.filter(user=request.user)
    return render(request, "store/orders.html", {
        "categories": Categorie.objects.all(),
        'userOrders': serializeUserOrders(userOrders)
    })

# API Views
def api_change_password(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    current_password = request.POST.get('password')
    new_password = request.POST.get('new_password')
    password_confirm = request.POST.get('password_confirmation')

    if not all([current_password, new_password, password_confirm]):
        return JsonResponse({"isOk": False, "error_type": "fields-invalid"})

    if new_password != password_confirm:
        return JsonResponse({"isOk": False, "error_type": "fields-invalid"})

    if not request.user.check_password(current_password):
        return JsonResponse({"isOk": False, "error_type": "password-invalid"})

    request.user.set_password(new_password)
    request.user.save()
    return JsonResponse({"isOk": True})

def api_change_addresses(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    try:
        Address.objects.update_or_create(
            user=request.user,
            defaults={
                "country": request.POST.get('country'),
                "city": request.POST.get('city'),
                "common": request.POST.get('common'),
                "quarter": request.POST.get('quarter'),
                "street_door": request.POST.get('streetDoor'),
                "zipcode": request.POST.get('zipcode'),
                "user": request.user
            }
        )
        return JsonResponse({"isOk": True})
    except:
        return JsonResponse({"isOk": False})

def api_change_profile_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    request.user.username = request.POST.get('username')
    request.user.email = request.POST.get('email')
    request.user.phone = request.POST.get('phone')
    request.user.save()
    return JsonResponse({"isOk": True})

def api_change_payment_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    method = json.loads(request.body).get('method')
    if not method:
        return JsonResponse({"isOk": False, "error_type": 'invalid-data'})

    PaymentMethod.objects.update_or_create(
        user=request.user,
        defaults={"method": method}
    )
    return JsonResponse({"isOk": True})

def api_get_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    # Get valid cart items and clean up any invalid ones
    userCart = Cart.objects.filter(user=request.user, ordered=False)
    
    # Remove any cart items with null products
    invalid_carts = userCart.filter(product__isnull=True)
    if invalid_carts.exists():
        invalid_carts.delete()
    
    # Get only valid cart items
    valid_cart = userCart.exclude(product__isnull=True)
    cart, cartSum = serializeCart(valid_cart)
    cartCount = valid_cart.count()

    return JsonResponse({
        "isOk": True,
        'cart': cart,
        'cartCount': cartCount,
        'cartSum': format_price(str(cartSum))
    })

def api_add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    data = json.loads(request.body)
    productID = data.get('productID')
    qty = data.get('qty', 1)

    if not productID:
        return JsonResponse({"isOk": False})

    product = Product.objects.filter(pk=productID).first()
    if not product:
        return JsonResponse({"isOk": False, 'error_type': "product-not-exist"})

    if Cart.objects.filter(user=request.user, product=product, ordered=False).exists():
        return JsonResponse({"isOk": False, 'error_type': "product-in-cart"})

    Cart.objects.create(
        user=request.user,
        product=product,
        quantity=qty,
        vendor=product.vendor
    )
    cartCount = Cart.objects.filter(user=request.user, ordered=False).count()
    return JsonResponse({"isOk": True, 'cartCount': cartCount})

def api_add_to_fav(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    productID = json.loads(request.body).get('productID')
    if not productID:
        return JsonResponse({"isOk": False})

    product = Product.objects.filter(pk=productID).first()
    if not product:
        return JsonResponse({"isOk": False, 'error_type': "product-not-exist"})

    wishList, created = WishList.objects.get_or_create(user=request.user)
    if wishList.product.filter(id=productID).exists():
        return JsonResponse({"isOk": False, 'error_type': "product-in-fav"})

    wishList.product.add(product)
    return JsonResponse({"isOk": True, 'wishCount': wishList.product.count()})

def api_order_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isOk": False, "error_type": "not-authenticated"})

    if request.method != 'POST':
        raise PermissionDenied()

    user = request.user
    if not user.phone:
        return JsonResponse({"isOk": False, "error_type": 'empty-phone'})

    if not Address.objects.filter(user=user).exists():
        return JsonResponse({"isOk": False, "error_type": 'empty-address'})

    userActivesCart = Cart.objects.filter(user=user, ordered=False)
    if not userActivesCart.exists():
        return JsonResponse({"isOk": False, "error_type": 'empty-cart'})

    # Get vendor's store
    try:
        vendor = user.vendor
        store = vendor.store
    except (Vendor.DoesNotExist, Store.DoesNotExist):
        return JsonResponse({"isOk": False, "error_type": 'invalid-vendor'})

    # Calculate total order amount
    total = sum(cart.product.price * cart.quantity for cart in userActivesCart)
    
    # Create order with all required fields
    order = Order.objects.create(
        user=user,
        total=total,
        store=store,
        customer=user,  # Since user is a Shopper
        status='pending'
    )
    
    # Add vendor to the order
    order.vendors.add(vendor)
    
    for cart in userActivesCart:
        cart.ordered = True
        cart.ordered_date = Date.today()
        cart.save()
        
        cart_product = Product.objects.filter(pk=cart.product.id).first()
        cart_product.sold_count += 1
        cart_product.save()
        
        order.cart.add(cart)

    return JsonResponse({"isOk": True})
