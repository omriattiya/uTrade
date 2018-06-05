from datetime import datetime

from DatabaseLayer import ShoppingCartDB, RegisteredUsers, PurchasedItems, Purchases, Owners
from DatabaseLayer.Discount import get_visible_discount, get_invisible_discount
from DatabaseLayer.Items import get_item
from DatabaseLayer.Lotteries import get_lottery, get_lottery_sum
from DatabaseLayer.Purchases import update_purchase_total_price
from DatabaseLayer.UserDetails import is_meet_conditions
from DomainLayer import ItemsLogic, LotteryLogic, ShoppingPolicyLogic
from ExternalSystems import ExternalSystems
from ServiceLayer.services.LiveAlerts import Consumer, PurchasesAlerts


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


def add_item_shopping_cart(login_token, shop_cart_item):
    if shop_cart_item.username is not None and shop_cart_item.item_id is not None and shop_cart_item.item_quantity > 0:
        if ItemsLogic.check_in_stock(shop_cart_item.item_id, shop_cart_item.item_quantity) is False:
            return False
        shopping_cart = Consumer.loggedInUsersShoppingCart[login_token]
        i = 0
        while i < len(shopping_cart):
            if shopping_cart[i].item_id == shop_cart_item.item_id:
                shopping_cart[i].item_quantity += shop_cart_item.item_quantity
                return True
            i = i + 1
        shopping_cart.append(shop_cart_item)
        return True
    return False


def update_item_shopping_cart(login_token, item_id, new_quantity):
    if login_token is not None and item_id is not None and new_quantity >= 0:
        username = Consumer.loggedInUsers[login_token]
        shopping_cart = Consumer.loggedInUsersShoppingCart[login_token]
        if new_quantity is 0:
            return remove_item_shopping_cart(username, item_id)
        if ItemsLogic.check_in_stock(item_id, new_quantity) is False:
            return False
        user = RegisteredUsers.get_user(username)
        if user is not False:
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


def update_code_shopping_cart(login_token, item_id, code):
    if login_token is not None and item_id is not None and code is not None:
        if len(code) == 15 and isinstance(code, str):
            shopping_cart = Consumer.loggedInUsersShoppingCart[login_token]
            i = 0
            while i < len(shopping_cart):
                if shopping_cart[i].item_id == item_id:
                    shopping_cart[i].code = code
                    return True
                i = i + 1
    return False


def check_empty_cart_user(login_token):
    shopping_cart = Consumer.loggedInUsersShoppingCart[login_token]
    return len(shopping_cart) == 0


def lottery_ending_check(lotteries):
    for lottery in lotteries:
        LotteryLogic.lottery_timer(lottery)


def pay_all(login_token):
    pay_confirmation = ''
    sup_confirmation = ''
    lotteries = []
    if login_token is not None:
        #  check if cart has items
        empty = check_empty_cart_user(login_token)
        if empty is not True:
            username = Consumer.loggedInUsers[login_token]
            to_create_purchase = True
            purchase_id = 0
            #  if so, check foreach item if the requested amount exist
            cart_items = get_cart_items(login_token)

            shopping_policy_status = shopping_policy_check(username, cart_items)
            if shopping_policy_status is not True:
                return shopping_policy_status

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
                if to_create_purchase is True:
                    to_create_purchase = False
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
                if item.kind == 'ticket':
                    if new_quantity == 0:
                        lotteries.append(item.id)
                status = ItemsLogic.update_stock(item.id, new_quantity)
                if status is False:
                    return 'Something went wrong with the purchase'
                # live alerts
                owners = Owners.get_owners_by_shop(item.shop_name)
                owners_name = []
                for owner in owners:
                    if owner.should_notify > 0:
                        owners_name.append(owner.username)
                PurchasesAlerts.notify_purchasing_alerts(owners_name,
                                                         '<strong>' + username + '</strong> has bought item <a href="http://localhost:8000/app/item/?item_id=' + str(
                                                             item.id) + '"># <strong>' + str(
                                                             item.id) + '</strong></a> from your shop')
            pay_confirmation = ExternalSystems.payment.pay(total_cost, username)
            if pay_confirmation is False:
                return 'Payment System Denied.'
            sup_confirmation = ExternalSystems.supply.supply_a_purchase(username, purchase_id)
            if sup_confirmation is False:
                return 'Supply System Denied.'
            remove_shopping_cart(login_token)
            status = ShoppingCartDB.remove_shopping_cart(username)
            lottery_ending_check(lotteries)
            if status:
                return [purchase_id, total_cost]
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
        if lottery.real_end_date is None:
            lotto_status = LotteryLogic.add_or_update_lottery_customer(cart_item.item_id,
                                                                           username,
                                                                           cart_item.item_quantity * item.price,
                                                                           cart_item.item_quantity)
            if lotto_status is False:
                return 'Something went wrong with the lottery ticket'
        else:
            return 'Lottery has ended'
    return True


def actual_pay(total_cost, username):
    return ExternalSystems.payment.pay(total_cost, username)


def supply_items(items):
    return ExternalSystems.supply.supply_my_items(items)


def get_cart_cost(login_token):
    empty = check_empty_cart_user(login_token)
    if empty is not True:
        #  if so, check foreach item if the requested amount exist
        cart_items = get_cart_items(login_token)
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
                    if lottery_sum + shopping_cart_item.item_quantity * item.price > lottery.max_price:
                        return False
                    else:
                        return False
                else:
                    return False
            total_cost = total_cost + shopping_cart_item.item_quantity * new_price
        return total_cost
    return False


def remove_shopping_cart(login_token):
    if login_token is not None:
        Consumer.loggedInUsersShoppingCart[login_token] = []


def remove_shopping_cart_db(username):
    return ShoppingCartDB.remove_shopping_cart(username)


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


def add_all_shopping_cart_to_user(shopping_cart):
    for cart_item in shopping_cart:
        status = ShoppingCartDB.add_item_shopping_cart(cart_item)
        if status is False:
            return False
        if cart_item.code is not None:
            status = ShoppingCartDB.update_code_shopping_cart(cart_item.username, cart_item.item_id, cart_item.code)
            if status is False:
                return False

    return True


def shopping_policy_check(username, cart_items):
    if not (username == "guest"):
        user = RegisteredUsers.get_user(username)
        if user is False:
            return "FAILED: User does not exist"
    id_status = check_identity_shopping_policies(username, cart_items)
    if id_status is not True:
        return id_status
    items_status = check_items_shopping_policies(username, cart_items)
    if items_status is not True:
        return items_status
    category_status = check_category_shopping_policies(username, cart_items)
    if category_status is not True:
        return category_status
    shop_status = check_shop_shopping_policies(username, cart_items)
    if shop_status is not True:
        return shop_status
    return True


def check_identity_shopping_policies(username, cart_items):
    identity_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_identity()
    for identity_policy in identity_policies:
        if not (username == "guest"):
            if is_meet_conditions(username, identity_policy.conditions) is False:
                continue
        if identity_policy.restriction == 'N':
            continue
        num_of_items = 0
        for cart_item in cart_items:
            num_of_items = num_of_items + cart_item.item_quantity
        if identity_policy.restriction == 'AL':
            if num_of_items < identity_policy.quantity:
                return "FAILED: Not enough items in cart; You allowed at least " + str(identity_policy.quantity)
        elif identity_policy.restriction == 'E':
            if num_of_items != identity_policy.quantity:
                return "FAILED: Not exact num of items in cart; You allowed exactly " + str(identity_policy.quantity)
        elif identity_policy.restriction == 'UT':
            if num_of_items > identity_policy.quantity:
                return "FAILED: Too much items in cart; You allowed at most " + str(identity_policy.quantity)
    return True


def check_items_shopping_policies(username, cart_items):
    items_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_items()
    for items_policy in items_policies:
        if not (username == "guest"):
            if is_meet_conditions(username, items_policy.conditions) is False:
                continue
        if items_policy.restriction == 'N':
            continue
        num_of_items = 0
        relevant = False
        cart_item_name = None
        for cart_item in cart_items:
            cart_item_name = ItemsLogic.get_item(cart_item.item_id).name
            if items_policy.item_name == cart_item_name:
                num_of_items = num_of_items + cart_item.item_quantity
                relevant = True
        if items_policy.restriction == 'AL':
            if relevant and num_of_items < items_policy.quantity:
                return "FAILED: Not enough " + cart_item_name + " items in cart; You allowed at least " + str(items_policy.quantity)
        elif items_policy.restriction == 'E':
            if relevant and num_of_items != items_policy.quantity:
                return "FAILED: Not exact num of " + cart_item_name + " items in cart; You allowed exactly " + str(items_policy.quantity)
        elif items_policy.restriction == 'UT':
            if relevant and num_of_items > items_policy.quantity:
                return "FAILED: Too much " + cart_item_name + " items in cart; You allowed at most " + str(items_policy.quantity)
    return True


def check_category_shopping_policies(username, cart_items):
    category_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_category()
    for category_policy in category_policies:
        if not (username == "guest"):
            if is_meet_conditions(username, category_policy.conditions) is False:
                continue
        if category_policy.restriction == 'N':
            continue
        num_of_items = 0
        relevant = False
        cart_item_category = None
        for cart_item in cart_items:
            cart_item_category = ItemsLogic.get_item(cart_item.item_id).category
            if category_policy.category == cart_item_category:
                num_of_items = num_of_items + cart_item.item_quantity
                relevant = True
        if category_policy.restriction == 'AL':
            if relevant and num_of_items < category_policy.quantity:
                return "FAILED: Not enough " + cart_item_category + " items in cart; You allowed at least " + str(category_policy.quantity)
        elif category_policy.restriction == 'E':
            if relevant and num_of_items != category_policy.quantity:
                return "FAILED: Not exact num of " + cart_item_category + " items in cart; You allowed exactly " + str(category_policy.quantity)
        elif category_policy.restriction == 'UT':
            if relevant and num_of_items > category_policy.quantity:
                return "FAILED: Too much " + cart_item_category + " items in cart; You allowed at most " + str(category_policy.quantity)
    return True


def check_shop_shopping_policies(username, cart_items):

    shop_policies = ShoppingPolicyLogic.get_all_shops_shopping_policies()
    for shop_policy in shop_policies:
        if not (username == "guest"):
            if is_meet_conditions(username, shop_policy.conditions) is False:
                continue
        if shop_policy.restriction == 'N':
            continue
        num_of_items = 0
        relevant = False
        cart_item_shop = None
        for cart_item in cart_items:
            cart_item_shop = ItemsLogic.get_item(cart_item.item_id).shop_name
            if shop_policy.shop_name == cart_item_shop:
                num_of_items = num_of_items + cart_item.item_quantity
                relevant = True
        if shop_policy.restriction == 'AL':
            if relevant and num_of_items < shop_policy.quantity:
                return "FAILED: Not enough " + cart_item_shop + " items in cart; You allowed at least " + str(shop_policy.quantity)
        elif shop_policy.restriction == 'E':
            if relevant and num_of_items != shop_policy.quantity:
                return "FAILED: Not exact num of " + cart_item_shop + " items in cart; You allowed exactly " + str(shop_policy.quantity)
        elif shop_policy.restriction == 'UT':
            if relevant and num_of_items > shop_policy.quantity:
                return "FAILED: Too much " + cart_item_shop + " items in cart; You allowed at most " + str(shop_policy.quantity)
    return True
