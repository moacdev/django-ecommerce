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
from django.urls import path
from django.conf.urls import handler400, handler403, handler404, handler500
from store.views import (
    categories, categoryProducts, homepage, login, product, 
    products, register, search, storeInfo, vendor_dashboard,
    vendor_add_product, vendor_edit_product, 
    product_detail, update_order_status,
    api_vendor_orders, api_vendor_products, update_vendor_settings,
    add_product_ajax, create_product, edit_product
)
from account import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage),
    path('connexion/', login),
    path('inscription/', register),
    path('categories/', categories),
    path('produits/', products),
    path('categories/<str:category>', categoryProducts),
    path('categories/<str:category>/<str:product>', product),
    path('recherche/', search),
    path('boutique/', storeInfo),

    # Account related URLs
    path('mon-compte/', account_views.account_info),
    path('liste-de-souhait', account_views.wish_list),
    path('mes-commandes', account_views.orders),
    path('commander-mon-panier/', account_views.order_cart),

    # API endpoints
    path('api/order-cart/', account_views.api_order_cart),
    path('api/account/change-password', account_views.api_change_password),
    path('api/account/change-addresses-info', account_views.api_change_addresses),
    path('api/account/change-profil-info', account_views.api_change_profile_info),
    path('api/account/change-payment-info', account_views.api_change_payment_info),
    path('api/get-cart', account_views.api_get_cart),
    path('api/add-to-cart', account_views.api_add_to_cart, name="add_to_cart"),
    path('api/add-to-fav', account_views.api_add_to_fav),

    path('admin/', admin.site.urls),
    path('vendor/dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('product/<slug:product_slug>/', product_detail, name='product_detail'),
    path('vendor/add-product/', vendor_add_product, name='vendor_add_product'),
    path('vendor/edit-product/<int:pk>/', vendor_edit_product, name='vendor_edit_product'),
    path('vendor/update-order-status/<int:order_id>/<str:status>/', update_order_status, name='update_order_status'),
    path('api/vendor/orders/', api_vendor_orders, name='api_vendor_orders'),
    path('api/vendor/orders/update-status/<int:order_id>/<str:status>/', api_vendor_orders, name='api_update_order_status'),
    path('api/vendor/products/', api_vendor_products, name='api_vendor_products'),
    path('vendor/update-settings/', update_vendor_settings, name='update_vendor_settings'),
    path('ajax/add-product/', add_product_ajax, name='add_product_ajax'),
    path('categories/<slug:category_slug>/<slug:product_slug>/', 
         product_detail, name='product_detail_with_category'),
    path('vendor/product/create/', create_product, name='create_product'),
    path('vendor/product/<slug:product_slug>/edit/', edit_product, name='edit_product'),
    path('api/vendor/order/update-status/', update_order_status, name='update_order_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'store.views.handler404'
handler403 = 'store.views.handler403'
handler500 = 'store.views.handler500'