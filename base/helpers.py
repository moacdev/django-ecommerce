import math

from store.models import Product, Categorie


def format_price(price: str):
    # Convert to string and handle any leading/trailing spaces
    price = str(price).strip()
    
    # Reverse the string to group from right to left
    reversed_price = price[::-1]
    
    # Split into groups of 3 and join with spaces
    groups = [reversed_price[i:i+3] for i in range(0, len(reversed_price), 3)]
    formatted_price = ' '.join(groups)
    
    # Reverse back to get the correct order
    return formatted_price[::-1]

def serializeCart(userCart):
    cart = []
    cartSum = 0
    for _cart in userCart:
        # Skip if product is None
        if not _cart.product:
            continue
        
        # get product from db and check if category is None
        product = Product.objects.get(id=_cart.product.id)
        category = Categorie.objects.get(id=product.category.id)
            
        # Skip if category is None
        if not category:
            continue
            
        try:
            cartSum += int(_cart.product.price)*int(_cart.quantity)
            _product = {
                'id': _cart.product.id,
                'label': _cart.product.label,
                'slug': _cart.product.slug,
                'stock': _cart.product.stock,
                'category_slug': category.slug,
                'category': category.label,
                'price_formatted': format_price(str(_cart.product.price)),
                'price': _cart.product.price,
                'image1': _cart.product.image1.url,
            }
            data = {
                'userID': _cart.user.id,
                'product': _product,
                'quantity': _cart.quantity
            }
            cart.append(data)
        except AttributeError as e:
            print("AttributeError", e)
            continue
            
    return cart, cartSum

def serializeWishList(userWishes):
    wish = []
    print(userWishes)
    if not userWishes or userWishes.product == None:
        return wish
    productsWished = userWishes.product.all()
    # wishSum = 0
    for _wish in productsWished:
        # userID = _wish.user.id
        # wishSum += int(_wish.product.price)
        _product = {
            'id': _wish.id,
            'label': _wish.label,
            'slug': _wish.slug,
            'stock': _wish.stock,
            'category_slug': _wish.category.slug,
            'category': _wish.category.label,
            'price': format_price(str(_wish.price)),
            'image1': _wish.image1.url,
        }
        wish.append(_product)
    return wish

def serializeProducts(_products):
    products = []
    
    # wishSum = 0
    for product in _products:
        # userID = product.user.id
        # wishSum += int(product.product.price)
        _product = {
            'id': product.id,
            'label': product.label,
            'slug': product.slug,
            'stock': product.stock,
            'category_slug': product.category.slug,
            'category': product.category.label,
            'price': format_price(str(product.price)),
            'image1': product.image1.url,
        }
        products.append(_product)
    return products

def serializeUserOrders(userOrders):
    orders = []

    for order in userOrders:
        carts, cartSum = serializeCart(order.cart.all())
        _order = {
            'carts': carts,
            'cartSum': cartSum,
            'code': order.code,
            'finished': order.finished,
            'ordered_date': order.ordered_date,
        }
        orders.append( _order )
    
    return orders




