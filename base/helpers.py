import math

from store.models import Product


def format_price(price: str):
    price_len = len(price)
    formated_price = price
    brk = 3
    price_brks = math.ceil(len(price) / brk)
    i = 0
    while i < price_brks:
        brk_computed = price_len - brk*i 
        i+=1
        if brk_computed == price_len or brk_computed == 0:
            continue
        formated_price = formated_price[:brk_computed] + '.' + formated_price[brk_computed:]
    return formated_price

def serializeCart(userCart):
    cart = []
    cartSum = 0
    for _cart in userCart:
        userID = _cart.user.id
        cartSum += int(_cart.product.price)*int(_cart.quantity)
        _product = {
            'id': _cart.product.id,
            'label': _cart.product.label,
            'slug': _cart.product.slug,
            'stock': _cart.product.stock,
            'category_slug': _cart.product.category.slug,
            'category': _cart.product.category.label,
            'price': format_price(str(_cart.product.price)),
            'image1': _cart.product.image1.url,
        }
        data = {
            'userID': userID,
            'product': _product,
            'quantity': _cart.quantity
        }
        cart.append(data)
    return cart, format_price(str(cartSum))

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




