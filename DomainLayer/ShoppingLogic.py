from DatabaseLayer import ShoppingCart


def remove_item_shopping_cart(username, item_id):
    if username is not None and item_id is not None:
        return ShoppingCart.remove_item_shopping_cart(username, item_id)


def browse_shopping_cart(username):
    if username is not None:
        return ShoppingCart.browse_shopping_cart(username)


def add_item_shopping_cart(user_id, item_id, quantity):
    if user_id is not None and item_id is not None and quantity > 0:
        return ShoppingCart.add_item(user_id, item_id, quantity)
