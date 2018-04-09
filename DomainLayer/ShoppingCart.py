from DatabaseLayer import ShoppingCart


def add_item_to_cart(user_id, item_id, quantity):
    if user_id is not None and item_id is not None and quantity > 0:
        return ShoppingCart.add_item_to_cart(user_id, item_id, quantity)
