from DatabaseLayer import ShoppingCart, RegisteredUsers
from DomainLayer import ItemsLogic


def remove_item_shopping_cart(username, item_id):
    if username is not None and item_id is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCart.remove_item_shopping_cart(username, item_id)


def get_cart_items(username):
    if username is not None:
        return ShoppingCart.get_cart_items(username)


def add_item_shopping_cart(username, item_id, quantity):
    if username is not None and item_id is not None and quantity > 0:
        if ItemsLogic.check_in_stock(item_id, quantity) is False:
            return False
        return ShoppingCart.add_item_shopping_cart(username, item_id, quantity)
    return False


def update_item_shopping_cart(username, item_id, new_quantity):
    if username is not None and item_id is not None and new_quantity >= 0:
        if new_quantity is 0:
            return remove_item_shopping_cart(username, item_id)
        if ItemsLogic.check_in_stock(item_id, new_quantity) is False:
            return False
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCart.update_item_shopping_cart(username, item_id, new_quantity)
    return False


def pay_all(username):
    if username is not None:
        #  check if cart has items
        empty = ShoppingCart.check_empty(username)
        if empty is not True:
            #  if so, check foreach item if the requested amount exist
            cart_items = get_cart_items(username)
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
