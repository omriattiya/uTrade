from datetime import datetime

from DatabaseLayer import ShoppingCartItem, RegisteredUsers, PurchasedItems, Purchases, Owners
from DatabaseLayer.Discount import get_visible_discount, get_invisible_discount
from DatabaseLayer.Items import get_item
from DatabaseLayer.Lotteries import get_lottery, get_lottery_sum
from DatabaseLayer.Purchases import update_purchase_total_price
from DomainLayer import ItemsLogic, LotteryLogic
from ExternalSystems import PaymentSystem, SupplySystem
from ServiceLayer import Consumer


def remove_item_shopping_cart(username, item_id):
    if username is not None and item_id is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCartItem.remove_item_shopping_cart(username, item_id)


def get_cart_items(username):
    if username is not None:
        return ShoppingCartItem.get_cart_items(username)


def add_item_shopping_cart(shop_cart_item):
    if shop_cart_item.username is not None and shop_cart_item.item_id is not None and shop_cart_item.item_quantity > 0:
        if ItemsLogic.check_in_stock(shop_cart_item.item_id, shop_cart_item.item_quantity) is False:
            return False
        existing = ShoppingCartItem.get_shopping_cart_item(shop_cart_item)
        if existing is not False:
            return update_item_shopping_cart(shop_cart_item.username, shop_cart_item.item_id,
                                             shop_cart_item.item_quantity + existing.item_quantity)
        else:
            return ShoppingCartItem.add_item_shopping_cart(shop_cart_item)
    return False


def update_item_shopping_cart(username, item_id, new_quantity):
    if username is not None and item_id is not None and new_quantity >= 0:
        if new_quantity is 0:
            return remove_item_shopping_cart(username, item_id)
        if ItemsLogic.check_in_stock(item_id, new_quantity) is False:
            return False
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCartItem.update_item_shopping_cart(username, item_id, new_quantity)
    return False


def update_code_shopping_cart(username, item_id, code):
    if username is not None and item_id is not None and code is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            if len(code) == 15 and isinstance(code, str):
                return ShoppingCartItem.update_code_shopping_cart(username, item_id, code)
    return False


def pay_all(username):
    if username is not None:
        #  check if cart has items
        empty = ShoppingCartItem.check_empty(username)
        if empty is not True:
            toCreatePurchase = True
            purchase_id = 0
            #  if so, check foreach item if the requested amount exist
            cart_items = get_cart_items(username)
            # cart_items is a array consist of shopping_cart objects
            for shopping_cart_item in cart_items:
                if ItemsLogic.check_in_stock(shopping_cart_item.item_id, shopping_cart_item.item_quantity) is False:
                    return False
            # if so, sum all items costs, get from costumer his credentials
            total_cost = 0
            # for each item, calculate visible_discount
            for shopping_cart_item in cart_items:
                item = get_item(shopping_cart_item.item_id)
                if shopping_cart_item.item_quantity > item.quantity:
                    return False
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
                lottery = get_lottery(item.id)
                if item.kind == 'ticket':
                    final_date = datetime.strptime(lottery.final_date, '%Y-%m-%d')
                    if final_date > datetime.now():
                        lottery_sum = get_lottery_sum(lottery.lotto_id)
                        if lottery_sum + shopping_cart_item.item_quantity * item.price < lottery.max_price:
                            lotto_status = LotteryLogic.add_or_update_lottery_customer(shopping_cart_item.item_id,
                                                                                       username,
                                                                                       shopping_cart_item.item_quantity * item.price)
                            if lotto_status is False:
                                return False
                        else:
                            return False
                    else:
                        return False
                total_cost = total_cost + shopping_cart_item.item_quantity * new_price
                if actual_pay(total_cost) is False:
                    return False
                # TODO make sure to reduce the amount of purchased items in shops & active shopping carts...

                if toCreatePurchase is True:
                    toCreatePurchase = False
                    purchase_id = Purchases.add_purchase_and_return_id(datetime.now(), username, 0)
                    if purchase_id is False:
                        return False
                status = PurchasedItems.add_purchased_item(purchase_id, shopping_cart_item.item_id,
                                                           shopping_cart_item.item_quantity,
                                                           shopping_cart_item.item_quantity * new_price)
                if status is False:
                    return False
                status = update_purchase_total_price(purchase_id, total_cost)
                if status is False:
                    return False
                new_quantity = item.quantity - shopping_cart_item.item_quantity
                status = ItemsLogic.update_stock(item.id, new_quantity)
                if status is False:
                    return False
                if supply_items(cart_items) is False:
                    return False
                # live alerts
                owners = Owners.get_owners_by_shop(item.shop_name)
                owners_name = []
                for owner in owners:
                    owners_name.append(owner.username)
                Consumer.notify_live_alerts(owners_name,
                                            '<strong>' + username + '</strong> has bought item <a href="../app/item/?item_id=' + item.id + '"># <strong>' + item.id + '</strong></a> from your shop')
            status = remove_shopping_cart(username)
            return status
    return False


def actual_pay(total_cost):
    return PaymentSystem.pay(total_cost)


def supply_items(items):
    return SupplySystem.supply_my_items(items)


def get_cart_cost(username):
    empty = ShoppingCartItem.check_empty(username)
    if empty is not True:
        #  if so, check foreach item if the requested amount exist
        cart_items = get_cart_items(username)
        # cart_items is a array consist of shopping_cart objects
        for shopping_cart_item in cart_items:
            if ItemsLogic.check_in_stock(shopping_cart_item.item_id, shopping_cart_item.item_quantity) is False:
                return False
        # if so, sum all items costs, get from costumer his credentials
        total_cost = 0
        # for each item, calculate visible_discount
        for shopping_cart_item in cart_items:
            item = get_item(shopping_cart_item.item_id)
            if shopping_cart_item.item_quantity > item.quantity:
                return False
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
            lottery = get_lottery(item.id)
            if item.kind == 'ticket':
                final_date = datetime.strptime(lottery.final_date, '%Y-%m-%d')
                if final_date > datetime.now():
                    lottery_sum = get_lottery_sum(lottery.lotto_id)
                    if lottery_sum + shopping_cart_item.item_quantity * item.price < lottery.max_price:
                        lotto_status = LotteryLogic.add_or_update_lottery_customer(shopping_cart_item.item_id,
                                                                                   username,
                                                                                   shopping_cart_item.item_quantity * item.price)
                        if lotto_status is False:
                            return False
                    else:
                        return False
                else:
                    return False
            total_cost = total_cost + shopping_cart_item.item_quantity * new_price
        return total_cost
    return False


def remove_shopping_cart(username):
    if username is not None:
        return ShoppingCartItem.remove_shopping_cart(username)

def get_user_purchases(username):
    return Purchases.get_user_purchases(username)


def get_purchased_items_by_purchase_id(purchase_id):
    return PurchasedItems.get_purchased_items_by_purchase(purchase_id)


def get_purchase(purchase_id):
    return Purchases.get_purchase(purchase_id)
