import math


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
        cartSum += _cart.product.price
        _product = {
            'label': _cart.product.label,
            'slug': _cart.product.label,
            'stock': _cart.product.stock,
            'price': format_price(str(_cart.product.price)),
            'image1': _cart.product.image1.url,
        }
        data = {
            'userID': userID,
            'product': _product,
            'quantity': _cart.quantity
        }
        cart.append(data)
    return cart, cartSum