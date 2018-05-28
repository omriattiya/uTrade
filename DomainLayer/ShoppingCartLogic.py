from datetime import datetime

from DatabaseLayer import ShoppingCartItem, RegisteredUsers, PurchasedItems, Purchases, Owners
from DatabaseLayer.Discount import get_visible_discount, get_invisible_discount
from DatabaseLayer.Items import get_item
from DatabaseLayer.Lotteries import get_lottery, get_lottery_sum
from DatabaseLayer.Purchases import update_purchase_total_price
from DomainLayer import ItemsLogic, LotteryLogic
from ExternalSystems import PaymentSystem, SupplySystem
from ServiceLayer import Consumer


def remove_item_shopping_cart(login_token, item_id):
    if login_token is not None and item_id is not None:
        shopping_cart_items = Consumer.loggedInUsersShoppingCart[login_token]
        i = 0
        while i < len(shopping_cart_items):
            if int(item_id) == shopping_cart_items[i].item_id:
                shopping_cart_items.remove(shopping_cart_items[i])
                return True
            i = i + 1
        return False


def get_cart_items(login_token):
    if login_token is not None:
        return Consumer.loggedInUsersShoppingCart[login_token]


def add_item_shopping_cart(login, shop_cart_item):
    if shop_cart_item.username is not None and shop_cart_item.item_id is not None and shop_cart_item.item_quantity > 0:
        if ItemsLogic.check_in_stock(shop_cart_item.item_id, shop_cart_item.item_quantity) is False:
            return False
        shopping_cart = Consumer.loggedInUsersShoppingCart[login]
        i = 0
        while i < len(shopping_cart):
            if shopping_cart[i].item_id == shop_cart_item.item_id:
                shopping_cart[i].item_quantity += shop_cart_item.item_quantity
                return True
            i = i + 1
            Consumer.loggedInUsersShoppingCart[login].append(shopping_cart)
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


def check_empty_cart_user(username):
    return ShoppingCartItem.check_empty(username)


def check_empty_cart_guest(username):
    return ShoppingCartItem.check_empty_guest(username)


def remove_shopping_cart_guest(guest):
    if guest is not None:
        return ShoppingCartItem.remove_shopping_cart_guest(guest)


def pay_all_guest(guest):
    if guest is not None:
        #  check if cart has items
        empty = ShoppingCartItem.check_empty_guest(guest)
        if empty is not True:
            toCreatePurchase = True
            purchase_id = 0
            #  if so, check foreach item if the requested amount exist
            cart_items = get_guest_shopping_cart_item(guest)
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
                if actual_pay(total_cost) is False:
                    return 'Something went wrong with the payment service'
                new_quantity = item.quantity - shopping_cart_item.item_quantity
                status = ItemsLogic.update_stock(item.id, new_quantity)
                if status is False:
                    return 'Something went wrong with the purchase'
                if supply_items(cart_items) is False:
                    return 'Something went wrong with the supply service'
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
                lottery_message = check_lottery_ticket(item, shopping_cart_item, username)
                if lottery_message is not True:
                    return lottery_message
                total_cost = total_cost + shopping_cart_item.item_quantity * new_price
                if actual_pay(total_cost) is False:
                    return 'Something went wrong with the payment service'
                # TODO make sure to reduce the amount of purchased items in shops & active shopping carts...

                if toCreatePurchase is True:
                    toCreatePurchase = False
                    purchase_id = Purchases.add_purchase_and_return_id(datetime.now(), username, 0)
                    if purchase_id is False:
                        return 'Something went wrong with the purchase'
                status = PurchasedItems.add_purchased_item(purchase_id, shopping_cart_item.item_id,
                                                           shopping_cart_item.item_quantity,
                                                           shopping_cart_item.item_quantity * new_price)
                if status is False:
                    return 'Something went wrong with the purchase'
                status = update_purchase_total_price(purchase_id, total_cost)
                if status is False:
                    return 'Something went wrong with the purchase'
                new_quantity = item.quantity - shopping_cart_item.item_quantity
                status = ItemsLogic.update_stock(item.id, new_quantity)
                if status is False:
                    return 'Something went wrong with the purchase'
                if supply_items(cart_items) is False:
                    return 'Something went wrong with the supply service'
                # live alerts
                owners = Owners.get_owners_by_shop(item.shop_name)
                owners_name = []
                for owner in owners:
                    owners_name.append(owner.username)
                Consumer.notify_live_alerts(owners_name,
                                            '<strong>' + username + '</strong> has bought item <a href="../app/item/?item_id=' + str(item.id) + '"># <strong>' + str(item.id) + '</strong></a> from your shop')
            status = remove_shopping_cart(username)
            if status is False:
                return 'Something went wrong with the purchase'
            else:
                return True
    return 'Shopping cart is empty'


def check_stock_for_shopping_cart(cart_items):
    for cart_item in cart_items:
        if ItemsLogic.check_in_stock(cart_item.item_id, cart_item.item_quantity) is False:
            item = ItemsLogic.get_item(cart_item.item_id)
            return 'Only ' + str(item.quantity) + ' ' + item.name + ' exist in the system'
    return True


def check_lottery_ticket(item, cart_item, username):
    if item.kind == 'ticket':
        lottery = get_lottery(item.id)
        final_date = datetime.strptime(lottery.final_date, '%Y-%m-%d')
        if final_date > datetime.now():
            lottery_sum = get_lottery_sum(lottery.lotto_id)
            if lottery_sum + cart_item.item_quantity * item.price < lottery.max_price:
                lotto_status = LotteryLogic.add_or_update_lottery_customer(cart_item.item_id,
                                                                           username,
                                                                           cart_item.item_quantity * item.price)
                if lotto_status is False:
                    return 'Something went wrong with the lottery ticket'
            else:
                return 'Purchase violates lottery policy'
        else:
            return 'Lottery has ended'
    return True


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


def order_of_guest(username):
    cart_items = get_guest_shopping_cart_item(username)
    return order_helper(cart_items)


def order_of_user(login_token):
    cart_items = Consumer.loggedInUsersShoppingCart[login_token]
    return order_helper(cart_items)


def order_helper(cart_items):
    items = []
    discount_prices = []
    total_prices = []
    number_of_items = 0
    if len(cart_items) == 0:
        return {'total_price': 0, 'cart_items_combined': cart_items, 'number_of_items': number_of_items}
    else:
        total_price = 0
        for i in range(0, len(cart_items)):
            item = get_item(cart_items[i].item_id)
            visible_discount = get_visible_discount(item.id, item.shop_name)
            percentage_visible = 0
            percentage_invisible = 0
            if visible_discount is not False:
                percentage_visible = visible_discount.percentage
            if cart_items[i].code is not None:
                invisible_discount = get_invisible_discount(item.id, item.shop_name, cart_items[i].code)
                percentage_invisible = invisible_discount.percentage
            discount_money = percentage_visible * item.price + percentage_invisible * (
                        1 - percentage_visible) * item.price
            discount_prices.append(discount_money)
            items.append(item)
            total_prices.append(item.price * cart_items[i].item_quantity - discount_money * cart_items[i].item_quantity)
            total_price = total_price + item.price * cart_items[i].item_quantity - discount_money * cart_items[
                i].item_quantity
            number_of_items = number_of_items + cart_items[i].item_quantity
        if cart_items is not False:
            return {'total_price': total_price,
                    'cart_items_combined': zip(cart_items, items, discount_prices, total_prices), 'number_of_items': number_of_items}


def get_new_guest_name():
        name = ShoppingCartItem.get_new_guest_name()
        if name is False:
            return 1
        else:
            return name.username + 1


def add_guest_item_shopping_cart(guest, item_id, quantity):
    return ShoppingCartItem.add_guest_shopping_cart(guest, item_id, quantity)


def get_guest_shopping_cart_item(username):
    return ShoppingCartItem.get_guest_shopping_cart_item(username)


def update_code_shopping_cart_guest(guest, item_id, code):
    if guest is not None and id is not None and code is not None:
        if len(code) == 15 and isinstance(code, str):
            return ShoppingCartItem.update_code_shopping_cart_guest(guest, item_id, code)
    return False


def remove_item_shopping_cart_guest(guest, item_id):
    if guest is not None and item_id is not None:
        return ShoppingCartItem.remove_item_shopping_cart_guest(guest, item_id)


def update_item_shopping_cart_guest(guest, item_id, new_quantity):
    if guest is not None and item_id is not None and new_quantity >= 0:
        if new_quantity is 0:
            return remove_item_shopping_cart_guest(guest, item_id)
        if ItemsLogic.check_in_stock(item_id, new_quantity) is False:
            return False
        return ShoppingCartItem.update_item_shopping_cart_guest(guest, item_id, new_quantity)
    return False
