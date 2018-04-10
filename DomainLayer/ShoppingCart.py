from DatabaseLayer import ShoppingCart


def remove_item_from_cart(username, item_id):
    if username is not None and item_id is not None:
        return ShoppingCart.remove_item_from_cart(username, item_id)


def browse_cart(username):
    if username is not None:
        return ShoppingCart.browse_cart(username)
