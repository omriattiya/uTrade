from datetime import datetime
from DatabaseLayer import ShoppingCart, RegisteredUsers, PurchasedItems
from DatabaseLayer.Discount import get_visible_discount, get_invisible_discount
from DatabaseLayer.Items import get_item
from DatabaseLayer.Lotteries import get_lottery,get_lottery_sum
from DomainLayer import ItemsLogic,LotteryLogic


def remove_item_shopping_cart(username, item_id):
    if username is not None and item_id is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            return ShoppingCart.remove_item_shopping_cart(username, item_id)


def get_cart_items(username):
    if username is not None:
        return ShoppingCart.get_cart_items(username)


def add_item_shopping_cart(shop_cart):
    if shop_cart.username is not None and shop_cart.item_id is not None and shop_cart.item_quantity > 0:
        if ItemsLogic.check_in_stock(shop_cart.item_id, shop_cart.item_quantity) is False:
            return False
        existing = ShoppingCart.get_shopping_cart_item(shop_cart)
        if existing is not False:
            return update_item_shopping_cart(shop_cart.username, shop_cart.item_id, shop_cart.item_quantity + existing.item_quantity)
        else:
            return ShoppingCart.add_item_shopping_cart(shop_cart)
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


def update_code_shopping_cart(username, item_id, code):
    if username is not None and item_id is not None and code is not None:
        user = RegisteredUsers.get_user(username)
        if user is not False:
            if len(code) == 15 and isinstance(code, str):
                return ShoppingCart.update_item_shopping_cart(username, item_id, code)
            print("bad code")
        print("No such user")
    return False


def pay_all(username):
    if username is not None:
        #  check if cart has items
        empty = ShoppingCart.check_empty(username)
        if empty is not True:
            #  if so, check foreach item if the requested amount exist
            cart_items = get_cart_items(username)
            # cart_items is a array consist of shopping_cart objects
            for shopping_cart in cart_items:
                if ItemsLogic.check_in_stock(shopping_cart.item_id, shopping_cart.item_quantity) is False:
                    return False
            # if so, sum all items costs, get from costumer his credentials
            total_cost = 0
            # for each item, calculate visible_discount
            for shopping_cart in cart_items:
                item = get_item(shopping_cart.item_id)
                if shopping_cart.item_quantity > item.quantity:
                    return False
                discount = get_visible_discount(item.id, item.shop_name)
                percentage = 0
                if discount is not False:
                    percentage = discount.percentage
                new_price = item.price * (1 - percentage)
                if shopping_cart.code is not None:
                    discount = get_invisible_discount(item.id, item.shop_name, shopping_cart.code)
                    if discount is not False:
                        percentage = discount.percentage
                    new_price = new_price * (1 - percentage)
                lottery = get_lottery(item.id)
                if item.kind == 'ticket':
                    final_date = datetime.strptime(lottery.final_date, '%Y-%m-%d')
                    if final_date > datetime.now():
                        lottery_sum = get_lottery_sum(lottery.lotto_id)
                        if lottery_sum + shopping_cart.item_quantity * item.price < lottery.max_price:
                            lotto_status = LotteryLogic.add_or_update_lottery_customer(shopping_cart.item_id, username, shopping_cart.item_quantity * item.price)
                            if lotto_status is False:
                                return False
                        else:
                            return False
                    else:
                        return False
                total_cost = total_cost + shopping_cart.item_quantity * new_price
                # TODO pay through the external payment system
                status = PurchasedItems.add_purchased_item(shopping_cart.item_id, datetime.now(),
                                                           shopping_cart.item_quantity,
                                                           shopping_cart.item_quantity * new_price,
                                                           shopping_cart.username)
                if status is False:
                    return False
                new_quantity = item.quantity - shopping_cart.item_quantity
                status = ItemsLogic.update_stock(item.id, new_quantity)
                if status is False:
                    return False
            return True
    return False
