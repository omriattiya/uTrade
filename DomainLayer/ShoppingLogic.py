from DatabaseLayer import ShoppingCart
from DomainLayer import ItemsLogic


def remove_item_shopping_cart(username, item_id):
    if username is not None and item_id is not None:
        return ShoppingCart.remove_item_shopping_cart(username, item_id)


def browse_shopping_cart(username):
    if username is not None:
        return ShoppingCart.browse_shopping_cart(username)


def add_item_shopping_cart(username, item_id, quantity):
    if username is not None and item_id is not None and quantity > 0:
        return ShoppingCart.add_item_shopping_cart(username, item_id, quantity)


def pay_all(username):
    if username is not None:
        #  check if cart has items
        empty = ShoppingCart.check_empty(username)
        if empty is not True:
            #  if so, check foreach item if the requested amount exist
            cart_items = browse_shopping_cart(username)
            for item_tuple in cart_items:
                if ItemsLogic.check_in_stock(item_tuple[1], item_tuple[2]) is False:
                    return False
            # if so, sum all items costs, get from costumer his credentials
            total_cost = 0
            for item_tuple in cart_items:
                total_cost = total_cost + item_tuple[2] * ItemsLogic.Items.get_item(item_tuple[1]).price
            # TODO pay through the external payment system
            return True
    return False
