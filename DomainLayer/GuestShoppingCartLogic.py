from DatabaseLayer import Owners
from DatabaseLayer.Items import get_item
from DomainLayer import ItemsLogic, UserShoppingCartLogic, LoggerLogic
from DomainLayer.DiscountLogic import get_visible_discount, get_invisible_discount
from DomainLayer.UserShoppingCartLogic import order_helper, check_lottery_ticket, check_stock_for_shopping_cart
from ExternalSystems import ExternalSystems
from ServiceLayer.services.LiveAlerts import Consumer, PurchasesAlerts
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
            purchase_id = 0
            #  if so, check foreach item if the requested amount exist
            cart_items = Consumer.guestShoppingCart[guest]
            # cart_items is a array consist of shopping_cart objects
            shopping_policy_status = UserShoppingCartLogic.shopping_policy_check("guest", cart_items)
            if shopping_policy_status is not True:
                return shopping_policy_status
            message = check_stock_for_shopping_cart(cart_items)
            if message is not True:
                return message
            # if so, sum all items costs, get from costumer his credentials
            total_cost = 0
            # for each item, calculate visible_discount
            for shopping_cart_item in cart_items:
                item = get_item(shopping_cart_item.item_id)
                new_price = UserShoppingCartLogic.get_new_price_for_item(item, shopping_cart_item)
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
                PurchasesAlerts.notify_purchasing_alerts(owners_name,
                                                         '<strong>' + guest + '</strong> has bought item <a href="http://localhost:8000/app/item/?item_id=' + str(
                                                             item.id) + '"># <strong>' + str(
                                                             item.id) + '</strong></a> from your shop')
            pay_confirmation = ExternalSystems.payment.pay(total_cost, guest)
            if pay_confirmation is False:
                return 'Payment System Denied.'
            sup_confirmation = ExternalSystems.supply.supply_a_purchase(guest, purchase_id)
            if sup_confirmation is False:
                return 'Supply System Denied.'
            status = remove_shopping_cart_guest(guest)
            if status is False:
                return 'Something went wrong with the purchase'
            LoggerLogic.add_event_log("GUEST", "PAY ALL")
            return [purchase_id, total_cost]
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
        if guest in Consumer.guestShoppingCart:
            shopping_cart = Consumer.guestShoppingCart[guest]
        else:
            Consumer.guestShoppingCart[guest] = []
            shopping_cart = Consumer.guestShoppingCart[guest]
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


def check_valid_cart(guest):
    shopping_cart = Consumer.guestShoppingCart[guest]
    i = 0
    if len(shopping_cart) == 0:
        return 'Shopping Cart Is Empty'
    while i < len(shopping_cart):
        item = get_item(shopping_cart[i].item_id)
        if item.shop_name != 'Active':
            return 'Item ', item.name, ' Is Unavailable Because Shop is Not Active'
        i = i + 1
    return True

