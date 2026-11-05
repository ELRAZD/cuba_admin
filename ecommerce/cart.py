from .models import Cart, CartItem, Product


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def add_to_cart(user, product_id, quantity=1):
    cart = get_or_create_cart(user)
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += int(quantity)
    else:
        item.quantity = int(quantity)
    item.save()
    return cart


def remove_from_cart(user, item_id):
    cart = get_or_create_cart(user)
    CartItem.objects.filter(cart=cart, id=item_id).delete()
    return cart


def clear_cart(user):
    cart = get_or_create_cart(user)
    cart.items.all().delete()