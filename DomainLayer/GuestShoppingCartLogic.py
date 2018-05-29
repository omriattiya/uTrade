from datetime import datetime

import SharedClasses
from DatabaseLayer import RegisteredUsers, PurchasedItems, Purchases, Owners, ShoppingCartDB
from DatabaseLayer.Discount import get_visible_discount, get_invisible_discount
from DatabaseLayer.Items import get_item
from DomainLayer import ItemsLogic
from DomainLayer.UserShoppingCartLogic import order_helper, check_lottery_ticket, check_stock_for_shopping_cart
from ExternalSystems import PaymentSystem, SupplySystem
from ServiceLayer import Consumer
from SharedClasses.ShoppingCartItem import ShoppingCartItem


def check_empty_cart_guest(guest):
    if guest is not None:
        return len(Consumer.guestShoppingCart[guest]) == 0
    return False


def remove_shopping_cart_guest(guest):
    if guest is not None:
        Consumer.guestShoppingCart = {}
        return True
    return False


def pay_all_guest(guest):
    if guest is not None:
        #  check if cart has items
        empty = check_empty_cart_guest(guest)
        if empty is not True:
            toCreatePurchase = True
            purchase_id = 0
            #  if so, check foreach item if the requested amount exist
            cart_items = Consumer.guestShoppingCart[guest]
            # cart_items is a array consist of shopping_cart objects
            message = check_stock_for_shopping_cart(cart_items)
            if message is not True:
                return message
            # if so, sum all items costs, get from costumer his credentials
            total_cost = 0
            # for each item, calculate visible_discount
            for shopping_cart_item in cart_items:
                item = get_item(shopping_cart_item.item_id)
                discount = get_visible_discount(item.id, item.shop_name)
                percentage = 0
                if discount is not False:
                    percentage = discount.percentage
                new_price = item.price * (1 - percentage)
                if shopping_cart_item.code is not None:
                    discount = get_invisible_discount(item.id, item.shop_name, shopping_cart_item.code)
                    if discount is not False:
                        percentage = discount.percentage
                    new_price = new_price * (1 - percentage)
                lottery_message = check_lottery_ticket(item, shopping_cart_item, guest)
                if lottery_message is not True:
                    return lottery_message
                total_cost = total_cost + shopping_cart_item.item_quantity * new_price
                new_quantity = item.quantity - shopping_cart_item.item_quantity
                status = ItemsLogic.update_stock(item.id, new_quantity)
                if status is False:
                    return 'Something went wrong with the purchase'
                # live alerts
                owners = Owners.get_owners_by_shop(item.shop_name)
                owners_name = []
                for owner in owners:
                    owners_name.append(owner.username)
                Consumer.notify_live_alerts(owners_name,
                                            '<strong>guest' + guest + '</strong> has bought item <a href="../app/item/?item_id=' + str(item.id) + '"># <strong>' + str(item.id) + '</strong></a> from your shop')
            status = remove_shopping_cart_guest(guest)
            if status is False:
                return 'Something went wrong with the purchase'
            else:
                return True
    return 'Shopping cart is empty'


def order_of_guest(guest):
    if guest is not None:
        cart_items = get_guest_shopping_cart_item(guest)
        return order_helper(cart_items)
    return False


def get_new_guest_name():
        Consumer.guestIndex += 1
        return 'guest' + (Consumer.guestIndex - 1)


def add_guest_item_shopping_cart(guest, item_id, quantity):
    if guest is not None and item_id is not None and quantity > 0:
        if ItemsLogic.check_in_stock(item_id, quantity) is False:
            return False
        if guest in Consumer.guestShoppingCart:
            shopping_cart = Consumer.guestShoppingCart[guest]
        else:
            Consumer.guestShoppingCart[guest] = []
            shopping_cart = Consumer.guestShoppingCart[guest]
        i = 0
        while i < len(shopping_cart):
            if shopping_cart[i].item_id == item_id:
                shopping_cart[i].item_quantity += quantity
                return True
            i = i + 1
        shopping_cart.append(ShoppingCartItem(guest, item_id, quantity, None))
        return True
    return False


def get_guest_shopping_cart_item(guest):
    if guest is not None:
        if guest in Consumer.guestShoppingCart:
            return Consumer.guestShoppingCart[guest]
        else:
            return {}
    return False


def update_code_shopping_cart_guest(guest, item_id, code):
    if guest is not None and item_id is not None and code is not None:
        if len(code) == 15 and isinstance(code, str):
            shopping_cart = Consumer.guestShoppingCart[guest]
            i = 0
            while i < len(shopping_cart):
                if shopping_cart[i].item_id == item_id:
                    shopping_cart[i].code = code
                    return True
                i = i + 1
    return False


def remove_item_shopping_cart_guest(guest, item_id):
    if guest is not None and item_id is not None:
        shopping_cart = Consumer.guestShoppingCart[guest]
        i = 0
        while i < len(shopping_cart):
            if shopping_cart[i].item_id == item_id:
                shopping_cart.remove(shopping_cart[i])
                return True
            i = i + 1
        return False


def update_item_shopping_cart_guest(guest, item_id, new_quantity):
    if guest is not None and item_id is not None and new_quantity >= 0:
        shopping_cart = Consumer.loggedInUsersShoppingCart[guest]
        if new_quantity is 0:
            return remove_item_shopping_cart_guest(guest, item_id)
        if ItemsLogic.check_in_stock(item_id, new_quantity) is False:
            return False
        i = 0
        while i < len(shopping_cart):
            if shopping_cart[i].item_id == item_id:
                if new_quantity == 0:
                    shopping_cart.remove(shopping_cart[i])
                    return True
                else:
                    shopping_cart[i].item_quantity = new_quantity
                    return True
            i = i + 1
    return False
