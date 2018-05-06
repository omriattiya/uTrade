from DatabaseLayer import Owners, SystemManagers
from DomainLayer import ItemsLogic
from DomainLayer import ShopLogic
from DomainLayer import ShoppingLogic
from DomainLayer import UsersLogic
from SharedClasses.Item import Item
from SharedClasses.Owner import Owner
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.ShoppingCartItem import ShoppingCartItem


def register_user(username, password):
    return UsersLogic.register((RegisteredUser(username, password)))


def login(username, password):
    return UsersLogic.login(RegisteredUser(username, password))


def open_shop(username, shop_name):
    return ShopLogic.create_shop(Shop(shop_name, 'Active'), username)


def is_owner(username, shop_name):
    return Owners.get_owner(username, shop_name) is not False


def add_item_to_shop(shop_name, item_name, item_category, keywords, price, quantity, username, kind, url):
    return ItemsLogic.add_item_to_shop(Item(0, shop_name, item_name, item_category, keywords, price, quantity, kind, url),
                                       username)


def buy_item(username, shop_name, item_id, quantity):
    return ShoppingLogic.add_item_shopping_cart(ShoppingCartItem(username, item_id, quantity, ""))


def is_item_bought(username, item_id):
    for item in ShoppingLogic.get_cart_items(username):
        if item.item_id == item_id:
            return True
    return False


def remove_item_from_cart(username, item_id):
    return ShoppingLogic.remove_item_shopping_cart(username, item_id)


def add_owner(owner, shop, new_owner):
    return UsersLogic.add_owner(owner, Owner(new_owner, shop, 1))


def edit_item_name(item_id, username, item_name):
    return ItemsLogic.edit_shop_item(username, item_id, 'name', item_name)


def search_shop(shop_name):
    return ShopLogic.search_shop(shop_name)


def pay_cart(username):
    return ShoppingLogic.pay_all(username)


def quantity_in_store(item_id):
    item = ItemsLogic.get_item(item_id)
    if item is not False:
        return item.quantity
    return False


def get_cart_cost(username):
    return ShoppingLogic.get_cart_cost(username)


def delete_user(by, who):
    return UsersLogic.remove_user(by, UsersLogic.get_registered_user(who))


def is_system_manager(username, password):
    return SystemManagers.login(username, password)
