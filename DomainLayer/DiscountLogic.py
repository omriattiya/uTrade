import datetime
import time

from DatabaseLayer import Owners, Discount, StoreManagers


def add_visible_discount(disc, username):
    if disc is not None and username is not None and disc.percentage >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_manager = StoreManagers.get_store_manager(username, disc.shop_name)
        if is_owner is not False or (is_manager is not False and is_manager.discount_permission == 1):
            return Discount.add_visible_discount(disc)
    return False


def add_invisible_discount(disc, username):
    if disc is not None and username is not None and disc.percentage >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_manager = StoreManagers.get_store_manager(username, disc.shop_name)
        if is_owner is not False or (is_manager is not False and is_manager.discount_permission == 1):
            return Discount.add_invisible_discount(disc)
    return False


def get_visible_discount(item_id, shop_name):
    if item_id is not None and shop_name is not None:
        discounts_arr = Discount.get_visible_discount(item_id, shop_name)
        if discounts_arr is False:
            return False
        now_time = time.time()
        for discount in discounts_arr:
            start_time = make_date_from_elements(discount.from_date)
            end_time = make_date_from_elements(discount.end_date)
            if start_time <= now_time < end_time:
                return discount
        return False
    return "FAILED: One (or more) of the parameters is None"


def get_invisible_discount(item_id, shop_name, text):
    if item_id is not None and shop_name is not None and text is not None:
        discounts_arr = Discount.get_invisible_discount(item_id, shop_name, text)
        if discounts_arr is False:
            return "FAILED: Discount retrieval failed."
        now_time = time.time()
        for discount in discounts_arr:
            start_time = make_date_from_elements(discount.from_date)
            end_time = make_date_from_elements(discount.end_date)
            if start_time <= now_time < end_time:
                return discount
        return False
    return "FAILED: One (or more) of the parameters is None"

# ___________________________________________ CATEGORY __________________________________________________________


def add_visible_discount_category(disc, username):
    if disc is not None and username is not None and disc.percentage >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_manager = StoreManagers.get_store_manager(username, disc.shop_name)
        if is_owner is not False or (is_manager is not False and is_manager.discount_permission == 1):
            return Discount.add_visible_discount_category(disc)
    return False


def add_invisible_discount_category(disc, username):
    if disc is not None and username is not None and disc.percentage >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_manager = StoreManagers.get_store_manager(username, disc.shop_name)
        if is_owner is not False or (is_manager is not False and is_manager.discount_permission == 1):
            return Discount.add_invisible_discount_category(disc)
    return False


def get_visible_discount_category(category, shop_name):
    if category is not None and shop_name is not None:
        discounts_arr = Discount.get_visible_discount_category(category, shop_name)
        if discounts_arr is False:
            return "FAILED: Discount retrieval failed."
        now_time = time.time()
        for discount in discounts_arr:
            start_time = make_date_from_elements(discount.from_date)
            end_time = make_date_from_elements(discount.end_date)
            if start_time <= now_time < end_time:
                return discount
        return False
    return "FAILED: One (or more) of the parameters is None"


def get_invisible_discount_category(category, shop_name, text):
    if category is not None and shop_name is not None and text is not None:
        discounts_arr = Discount.get_invisible_discount_category(category, shop_name, text)
        if discounts_arr is False:
            return "FAILED: Discount retrieval failed."
        now_time = time.time()
        for discount in discounts_arr:
            start_time = make_date_from_elements(discount.from_date)
            end_time = make_date_from_elements(discount.end_date)
            if start_time <= now_time < end_time:
                return discount
        return False
    return "FAILED: One (or more) of the parameters is None"


def make_date_from_elements(date_string):
    dt = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    date_time = time.mktime(dt.timetuple())
    return date_time
