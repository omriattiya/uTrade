from datetime import datetime

from DatabaseLayer import ShoppingCartDB, RegisteredUsers, Purchases
from DatabaseLayer.Discount import get_visible_discount, get_invisible_discount
from DatabaseLayer.Items import get_item
from DatabaseLayer.Lotteries import get_lottery, get_lottery_sum
from DatabaseLayer.UserDetails import is_meet_conditions
from DomainLayer import ItemsLogic, LotteryLogic
from DomainLayer import ShoppingPolicyLogic


def remove_item_shopping_cart(username, item_id):
    if username is not None and item_id is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCartDB.remove_item_shopping_cart(username, item_id)


def get_cart_items(username):
    if username is not None:
        return ShoppingCartDB.get_cart_items(username)


def add_item_shopping_cart(shop_cart_item):
    if shop_cart_item.username is not None and shop_cart_item.item_id is not None and shop_cart_item.item_quantity > 0:
        if ItemsLogic.check_in_stock(shop_cart_item.item_id, shop_cart_item.item_quantity) is False:
            return False
        existing = ShoppingCartDB.get_shopping_cart_item(shop_cart_item)
        if existing is not False:
            return update_item_shopping_cart(shop_cart_item.username, shop_cart_item.item_id,
                                             shop_cart_item.item_quantity + existing.item_quantity)
        else:
            return ShoppingCartDB.add_item_shopping_cart(shop_cart_item)
    return False


def update_item_shopping_cart(username, item_id, new_quantity):
    if username is not None and item_id is not None and new_quantity >= 0:
        if new_quantity is 0:
            return remove_item_shopping_cart(username, item_id)
        if ItemsLogic.check_in_stock(item_id, new_quantity) is False:
            return False
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCartDB.update_item_shopping_cart(username, item_id, new_quantity)
    return False


def update_code_shopping_cart(username, item_id, code):
    if username is not None and item_id is not None and code is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            if len(code) == 15 and isinstance(code, str):
                return ShoppingCartDB.update_code_shopping_cart(username, item_id, code)
    return False


def check_empty_cart_user(username):
    return ShoppingCartDB.check_empty(username)


def check_stock_for_shopping_cart(cart_items):
    for cart_item in cart_items:
        if ItemsLogic.check_in_stock(cart_item.item_id, cart_item.item_quantity) is False:
            item = ItemsLogic.get_item(cart_item.item_id)
            return 'Only ' + str(item.quantity) + ' ' + item.name + ' exist in the system'
    return True


def remove_shopping_cart(username):
    if username is not None:
        return ShoppingCartDB.remove_shopping_cart(username)


def get_user_purchases(username):
    return Purchases.get_user_purchases(username)


def get_purchased_items_by_purchase_id(purchase_id):
    return Purchases.get_purchased_items_by_purchase(purchase_id)


def get_purchase(purchase_id):
    return Purchases.get_purchase(purchase_id)


def order_of_user(username):
    cart_items = get_cart_items(username)
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


def shopping_policy_check(username, cart_items):
    if username is not "guest":
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
        if username is not "guest":
            if is_meet_conditions(username, identity_policy.conditions) is False:
                continue
        if identity_policy.restriction is 'N':
            continue
        elif identity_policy.restriction is 'AL':
            if len(cart_items) < identity_policy.quantity:
                return "FAILED: Not enough items in cart; You allowed at least " + identity_policy.quantity
        elif identity_policy.restriction is 'E':
            if len(cart_items) != identity_policy.quantity:
                return "FAILED: Not exact num of items in cart; You allowed exactly " + identity_policy.quantity
        elif identity_policy.restriction is 'UT':
            if len(cart_items) > identity_policy.quantity:
                return "FAILED: Too much items in cart; You allowed at most " + identity_policy.quantity
    return True


def check_items_shopping_policies(username, cart_items):
    items_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_items()
    for items_policy in items_policies:
        if username is not "guest":
            if is_meet_conditions(username, items_policy.conditions) is False:
                continue
        if items_policy.restriction is 'N':
            continue
        num_of_items = 0
        cart_item_name = None
        for cart_item in cart_items:
            cart_item_name = ItemsLogic.get_item(cart_item.item_id).name
            if items_policy.item_name == cart_item_name:
                num_of_items = num_of_items + cart_item.item_quantity
        if items_policy.restriction is 'AL':
            if num_of_items < items_policy.quantity:
                return "FAILED: Not enough " + cart_item_name + " items in cart; You allowed at least " + items_policy.quantity
        elif items_policy.restriction is 'E':
            if num_of_items != items_policy.quantity:
                return "FAILED: Not exact num of " + cart_item_name + " items in cart; You allowed exactly " + items_policy.quantity
        elif items_policy.restriction is 'UT':
            if num_of_items > items_policy.quantity:
                return "FAILED: Too much " + cart_item_name + " items in cart; You allowed at most " + items_policy.quantity
    return True


def check_category_shopping_policies(username, cart_items):
    category_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_category()
    for category_policy in category_policies:
        if username is not "guest":
            if is_meet_conditions(username, category_policy.conditions) is False:
                continue
        if category_policy.restriction is 'N':
            continue
        num_of_items = 0
        cart_item_category = None
        for cart_item in cart_items:
            cart_item_category = ItemsLogic.get_item(cart_item.item_id).category
            if category_policy.category == cart_item_category:
                num_of_items = num_of_items + cart_item.item_quantity
        if category_policy.restriction is 'AL':
            if num_of_items < category_policy.quantity:
                return "FAILED: Not enough " + cart_item_category + " items in cart; You allowed at least " + category_policy.quantity
        elif category_policy.restriction is 'E':
            if num_of_items != category_policy.quantity:
                return "FAILED: Not exact num of " + cart_item_category + " items in cart; You allowed exactly " + category_policy.quantity
        elif category_policy.restriction is 'UT':
            if num_of_items > category_policy.quantity:
                return "FAILED: Too much " + cart_item_category + " items in cart; You allowed at most " + category_policy.quantity
    return True


def check_shop_shopping_policies(username, cart_items):
    shop_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_shop()
    for shop_policy in shop_policies:
        if username is not "guest":
            if is_meet_conditions(username, shop_policy.conditions) is False:
                continue
        if shop_policy.restriction is 'N':
            continue
        num_of_items = 0
        cart_item_shop = None
        for cart_item in cart_items:
            cart_item_shop = ItemsLogic.get_item(cart_item.item_id).shop_name
            if shop_policy.category == cart_item_shop:
                num_of_items = num_of_items + cart_item.item_quantity
        if shop_policy.restriction is 'AL':
            if num_of_items < shop_policy.quantity:
                return "FAILED: Not enough " + cart_item_shop + " items in cart; You allowed at least " + shop_policy.quantity
        elif shop_policy.restriction is 'E':
            if num_of_items != shop_policy.quantity:
                return "FAILED: Not exact num of " + cart_item_shop + " items in cart; You allowed exactly " + shop_policy.quantity
        elif shop_policy.restriction is 'UT':
            if num_of_items > shop_policy.quantity:
                return "FAILED: Too much " + cart_item_shop + " items in cart; You allowed at most " + shop_policy.quantity
    return True
