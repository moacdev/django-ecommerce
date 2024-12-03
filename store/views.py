import math
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from django.template import RequestContext
from account.models import Shopper
from base.helpers import format_price, serializeProducts
from store.models import Categorie, Product, Order
from django.core.validators import validate_email
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Store
from .forms import ProductForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from .models import Vendor
from django.db import transaction
from django.views.decorators.http import require_POST
from django.http import Http404
from django.views.decorators.http import require_http_methods
import json





def homepage(request):
    products = Product.objects.all()
    for _product in products:
        _product.price = format_price(str(_product.price))
    
    most_sold = products.order_by('-sold_count')
    most_viewed = products.order_by('-views_count')
        
    return render(request, 'store/index.html', { "categories": Categorie.objects.all(), "products": products.order_by('-id'), 'most_sold' : most_sold, 'most_viewed': most_viewed })

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember-me")
        
        if login and password:
            user = authenticate(request, username=login, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Set session expiry based on remember-me
                if not remember_me:
                    request.session.set_expiry(0)  # Browser session only
                
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                return render(request, "store/login.html", {
                    "error": "Invalid credentials",
                    "email": login
                })
    
    return render(request, "store/login.html", {
        "error": None,
        "email": ""
    })

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        
        # Validate all fields are present
        if not all([email, username, phone, password, password_confirmation]):
            return render(request, "store/register.html", {
                "error": "All fields are required.",
                "email": email,
                "username": username,
                "phone": phone
            })
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return render(request, "store/register.html", {
                "error": "Invalid email format.",
                "email": email,
                "username": username,
                "phone": phone
            })
        
        # Check if passwords match
        if password != password_confirmation:
            return render(request, "store/register.html", {
                "error": "Passwords do not match.",
                "email": email,
                "username": username,
                "phone": phone
            })
        
        # Check if email or username already exists
        if Shopper.objects.filter(email=email).exists():
            return render(request, "store/register.html", {
                "error": "Email already in use.",
                "email": email,
                "username": username,
                "phone": phone
            })
        
        if Shopper.objects.filter(username=username).exists():
            return render(request, "store/register.html", {
                "error": "Username already taken.",
                "email": email,
                "username": username,
                "phone": phone
            })
        
        try:
            # Wrap the entire creation process in a transaction
            with transaction.atomic():
                # Create the user
                user = Shopper.objects.create_user(username, email, password)
                user.phone = phone
                user.save()

                # Create a store for the user
                store = Store.objects.create(
                    name=f"{username}'s Store",
                    owner=user
                )

                # Create a vendor profile
                vendor = Vendor.objects.create(
                    user=user,
                    name=username,
                    store=store
                )

                # Verify the vendor was created
                if not hasattr(user, 'vendor'):
                    raise Exception("Vendor account creation failed")

                auth_login(request, user)
                return redirect('/')

        except Exception as e:
            # If anything fails, roll back the transaction
            return render(request, "store/register.html", {
                "error": f"Registration failed: {str(e)}",
                "email": email,
                "username": username,
                "phone": phone
            })
    
    return render(request, "store/register.html")

def logout_view(request):
    logout(request)
    return redirect('/')

def categories(request):
    return render(request, "store/categories.html", { "categories": Categorie.objects.all() })

def products(request):
    categories = Categorie.objects.all()
    if  request.GET.get('categorie'):
        category = get_object_or_404(Categorie, slug=request.GET.get('categorie'))
        products = Product.objects.filter(category=category)
        productCount = products.count()
    else:
        products = Product.objects.all()
        productCount = products.count()

    currentPage = 1
    if request.GET.get('page'):
        currentPage = int(request.GET.get('page'))
    
    productPerPage = 25
    corners = 1
    totalPages = math.ceil(productCount / productPerPage)

    
    take_from = productPerPage * (currentPage-1)

    

    pagination = {
        'totalPages' : list(range(1,totalPages+1)),
        'productPerPage' : productPerPage,
        'currentPage': currentPage,
        'corners': list(range(1,corners+1))
    }



    return render(request, "store/products.html", {'pagination': pagination, 'productCount': productCount, "categories": Categorie.objects.all(), 'products': serializeProducts(products)[take_from:take_from+productPerPage] })

def categoryProducts(request, category):
    categories = Categorie.objects.all()
    
    _category = get_object_or_404(Categorie, slug=category)
    products = Product.objects.filter(category=_category)
    productCount = products.count()

    currentPage = 1
    if request.GET.get('page'):
        currentPage = int(request.GET.get('page'))
    
    productPerPage = 25
    corners = 1
    totalPages = math.ceil(productCount / productPerPage)

    
    take_from = productPerPage * (currentPage-1)

    

    pagination = {
        'totalPages' : list(range(1,totalPages+1)),
        'productPerPage' : productPerPage,
        'currentPage': currentPage,
        'corners': list(range(1,corners+1))
    }

    return render(request, "store/category-products.html", {'pagination': pagination, 'productCount': productCount, "categories": Categorie.objects.all(), 'products': serializeProducts(products)[take_from:take_from+productPerPage] })

def product(request, category, product):
    _category = get_object_or_404(Categorie, slug=category)
    _product = get_object_or_404(Product, slug=product, category=_category.id)
    _product.views_count += 1
    _product.save()
    return render(request, "store/view_product.html", { "categories": Categorie.objects.all(), "category": _category, "product": _product })

def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    return render(request, "store/search_results.html", {
        "categories": Categorie.objects.all(),
        "products": products,
        "query": query
    })

def storeInfo(request):
    return render(request, "store/store_info.html", {
        "categories": Categorie.objects.all()
    })

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

@login_required
def vendor_dashboard(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
        return render(request, 'store/vendor_dashboard.html', {
            'vendor': vendor,
            'active_tab': 'products'
        })
    except Vendor.DoesNotExist:
        messages.error(request, "You need a vendor account to access the dashboard.")
        return redirect('home')

@login_required
def api_vendor_orders(request):
    page = request.GET.get('page', 1)
    
    # Get the vendor instance associated with the user
    try:
        vendor = request.user.vendor
        orders = Order.objects.filter(store=vendor.store).distinct()
        print(orders)
        
        paginator = Paginator(orders, 10)
        orders_page = paginator.get_page(page)
        
        data = {
            'orders': [{
                'id': order.id,
                'customer': order.customer.get_full_name() if order.customer else 'Anonymous',
                'total': str(order.total),
                'status': order.status,
                'date': order.ordered_date.strftime('%Y-%m-%d %H:%M'),
                'products': [
                    {
                        'name': cart.product.label,
                        'quantity': cart.quantity
                    } for cart in order.cart.all()
                ]
            } for order in orders_page],
            'has_next': orders_page.has_next(),
            'has_previous': orders_page.has_previous(),
            'total_pages': paginator.num_pages,
            'current_page': int(page),
        }
        return JsonResponse(data)
    
    except AttributeError as e:
        print(e)
        return JsonResponse({
            'error': 'User is not associated with a vendor account',
            'orders': [],
            'has_next': False,
            'has_previous': False,
            'total_pages': 0,
            'current_page': 1
        })

@login_required
def api_vendor_products(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
        products = Product.objects.filter(vendor=vendor).order_by('-created_at')
        
        paginator = Paginator(products, 12)
        page = request.GET.get('page', 1)
        products_page = paginator.get_page(page)
        
        data = {
            'products': [{
                'id': product.id,
                'name': product.label,
                'slug': product.slug,
                'price': str(product.price),
                'stock': product.stock,
                'status': product.get_status_display(),
                'url': product.get_absolute_url(),
                'image1': product.image1.url if product.image1 else None,
                'image2': product.image2.url if product.image2 else None,
                'image3': product.image3.url if product.image3 else None,
                'image4': product.image4.url if product.image4 else None,
            } for product in products_page],
            'has_next': products_page.has_next(),
            'has_previous': products_page.has_previous(),
            'total_pages': paginator.num_pages,
            'current_page': int(page),
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'products': [],
            'has_next': False,
            'has_previous': False,
            'total_pages': 0,
            'current_page': 1
        }, status=400)

@login_required
def vendor_add_product(request):
    if request.method == 'POST':
        try:
            # Get the vendor associated with the current user
            vendor = request.user.vendor  # Adjust this according to your user-vendor relationship
            
            # Create product instance
            product = Product(
                vendor=vendor,
                store=vendor.store,
                label=request.POST['label'],
                description=request.POST['description'],
                price=request.POST['price'],
                stock=request.POST['stock'],
            )
            
            # Handle category
            if request.POST.get('category') == 'other':
                # Create new category if 'other' was selected
                new_category = Categorie.objects.create(label=request.POST['new_category'])
                product.category = new_category
            else:
                product.category = Categorie.objects.get(id=request.POST['category'])
            
            # Handle image uploads
            if request.FILES.get('image1'):
                product.image1 = request.FILES['image1']
            if request.FILES.get('image2'):
                product.image2 = request.FILES['image2']
            if request.FILES.get('image3'):
                product.image3 = request.FILES['image3']
            if request.FILES.get('image4'):
                product.image4 = request.FILES['image4']
            
            product.save()
            
            return JsonResponse({'status': 'success', 'message': 'Product added successfully'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def vendor_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, vendor=request.user.vendor)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
    return redirect('vendor_dashboard')

@login_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id, product__vendor=request.user.vendor)
    order.status = status
    order.save()
    
    # Send email notification
    send_mail(
        f'Order #{order.id} Status Update',
        f'Your order status has been updated to: {status}',
        settings.DEFAULT_FROM_EMAIL,
        [order.customer.email],
        fail_silently=True,
    )
    
    return JsonResponse({'status': 'success'})

def order_list(request):
    orders = Order.objects.filter(product__vendor=request.user.vendor)
    return render(request, 'store/order_list.html', {'orders': orders})

def change_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    order.status = status
    order.save()
    send_order_notification(order)
    return redirect('order_list')

def send_order_notification(order):
    subject = f"Order {order.id} Status Changed"
    message = f"The status of your order {order.id} has been changed to {order.status}."
    recipient_list = [order.customer.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

@login_required
def product_detail(request, product_slug, category_slug=None):
    try:
        if category_slug:
            # If category is specified in URL, ensure product belongs to that category
            product = get_object_or_404(
                Product.objects.select_related('category', 'vendor'),
                slug=product_slug,
                category__slug=category_slug,
                # status='ACTIVE'  # Only show active products
            )
        else:
            # Direct product URL
            product = get_object_or_404(
                Product.objects.select_related('category', 'vendor'),
                slug=product_slug,
                # status='ACTIVE'
            )

        context = {
            'product': product,
            'related_products': Product.objects.filter(
                category=product.category,
                # status='ACTIVE'
            ).exclude(id=product.id)[:4]
        }
        
        return render(request, 'store/product_detail.html', context)

    except Http404:
        # Handle 404 errors gracefully
        return render(request, 'store/404.html', status=404)

@login_required
def update_vendor_settings(request):
    if request.method == 'POST':
        try:
            vendor = Vendor.objects.get(user=request.user)
            vendor.name = request.POST.get('store_name')
            if 'logo' in request.FILES:
                vendor.logo = request.FILES['logo']
            vendor.save()
            messages.success(request, 'Settings updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating settings: {str(e)}')
    return redirect('vendor_dashboard')

def get_vendor_products(request):
    vendor = request.user.vendor
    products = Product.objects.filter(vendor=vendor)
    
    products_data = [{
        'id': product.id,
        'name': product.label,  # or however you name your product
        'price': product.price,
        'image1': product.image1.url if product.image1 and hasattr(product.image1, 'url') else '',
        'image2': product.image2.url if product.image2 and hasattr(product.image2, 'url') else '',
        'image3': product.image3.url if product.image3 and hasattr(product.image3, 'url') else '',
        'image4': product.image4.url if product.image4 and hasattr(product.image4, 'url') else '',
        # ... other product fields ...
    } for product in products]
    
    return JsonResponse({
        'products': products_data,
        'total_pages': 1,  # Add pagination if needed
        'current_page': 1
    })

@require_POST
def add_product_ajax(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
        label = request.POST.get('label')
        category_id = request.POST.get('category')
        new_category = request.POST.get('new_category', None)
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2', None)
        image3 = request.FILES.get('image3', None)
        image4 = request.FILES.get('image4', None)

        # Handle category logic
        if new_category:
            category = Categorie.objects.create(label=new_category)
        else:
            category = Categorie.objects.get(id=category_id)

        product = Product.objects.create(
            vendor=vendor,
            label=label,
            category=category,
            price=price,
            stock=stock,
            description=description,
            status='PENDING',  # Set initial status
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4
        )

        return JsonResponse({
            'success': True, 
            'product_id': product.id,
            'status': product.get_status_display()  # This will return the human-readable status
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
@login_required
def change_product_status(request, product_id):
    try:
        product = Product.objects.get(id=product_id, vendor=request.user.vendor)
        new_status = request.POST.get('status')
        
        if new_status in dict(Product.STATUS_CHOICES):
            product.status = new_status
            product.save()
            
            return JsonResponse({
                'success': True,
                'status': product.get_status_display(),
                'status_code': product.status
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid status'
            }, status=400)
            
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Product not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def create_product(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except Vendor.DoesNotExist:
        messages.error(request, "You need a vendor account to create products.")
        return redirect('home')

    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            new_category = request.POST.get('new_category')
            
            if new_category:
                # Check if category already exists by label
                category = Categorie.objects.filter(label=new_category).first()
                if not category:
                    _ = Categorie.objects.create(label=new_category)
                    print(_)
            else:
                category = Categorie.objects.get(id=category_id)

            product = Product.objects.create(
                vendor=vendor,
                category=category,
                label=request.POST.get('label'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                stock=request.POST.get('stock'),
                image1=request.FILES.get('image1'),
                image2=request.FILES.get('image2') if 'image2' in request.FILES else None,
                image3=request.FILES.get('image3') if 'image3' in request.FILES else None,
                image4=request.FILES.get('image4') if 'image4' in request.FILES else None,
            )
            
            messages.success(request, 'Product created successfully!')
            return redirect('vendor_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    categories = Categorie.objects.all()
    return render(request, 'store/product_form.html', {
        'categories': categories,
        'action': 'Create'
    })

@login_required
def edit_product(request, product_slug):
    try:
        vendor = Vendor.objects.get(user=request.user)
        product = get_object_or_404(Product, slug=product_slug, vendor=vendor)
    except Vendor.DoesNotExist:
        messages.error(request, "You need a vendor account to edit products.")
        return redirect('home')

    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            new_category = request.POST.get('new_category')
            
            if new_category:
                category, _ = Categorie.objects.get_or_create(label=new_category)
            else:
                category = Categorie.objects.get(id=category_id)

            product.category = category
            product.label = request.POST.get('label')
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')
            product.stock = request.POST.get('stock')

            if 'image1' in request.FILES:
                product.image1 = request.FILES['image1']
            if 'image2' in request.FILES:
                product.image2 = request.FILES['image2']
            if 'image3' in request.FILES:
                product.image3 = request.FILES['image3']
            if 'image4' in request.FILES:
                product.image4 = request.FILES['image4']

            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('vendor_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    categories = Categorie.objects.all()
    return render(request, 'store/product_form.html', {
        'product': product,
        'categories': categories,
        'action': 'Edit'
    })

@require_http_methods(["POST"])
def update_order_status(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')

        # Verify the vendor owns this order
        order = Order.objects.filter(
            id=order_id,
            vendors=request.user.vendor
        ).first()

        if not order:
            return JsonResponse({
                'success': False,
                'error': 'Order not found'
            })

        # Validate status
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': 'Invalid status'
            })

        # Update the order
        order.status = new_status
        order.save()

        return JsonResponse({
            'success': True
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
