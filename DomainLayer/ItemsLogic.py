from DatabaseLayer import Items, StoreManagers, ReviewsOnItems, Owners, SystemManagers
from DatabaseLayer import PurchasedItems
from DatabaseLayer.Items import update_item


def add_item_to_shop(item, username):
    if item is not None and item.shop_name is not None and username is not None and item.quantity >= 0 \
            and item.price >= 0:
        manager = StoreManagers.get_store_manager(username, item.shop_name)
        if manager is not False:
            add_item_permission = manager.permission_add_item
            if add_item_permission > 0:
                return Items.add_item_to_shop(item)
        if Owners.get_owner(username, item.shop_name) is not False:
            return Items.add_item_to_shop(item)
    return False


def add_item_to_shop_and_return_id(item, username):
    if item is not None and item.shop_name is not None and username is not None and item.quantity >= 0 \
            and item.price >= 0:
        manager = StoreManagers.get_store_manager(username, item.shop_name)
        if manager is not False:
            add_item_permission = manager.permission_add_item
            if add_item_permission > 0:
                return Items.add_item_to_shop_and_return_id(item)
        if Owners.get_owner(username, item.shop_name) is not False:
            return Items.add_item_to_shop_and_return_id(item)
    return False


def remove_item_from_shop(item_id, username):
    if item_id is not None:
        item = Items.get_item(item_id)
        if item is not False:
            manager = StoreManagers.get_store_manager(username, item.shop_name)
            if manager is not False:
                remove_item_permission = manager.permission_remove_item
                if remove_item_permission > 0:
                    return Items.remove_item_from_shop(item_id)
            elif Owners.is_owner(username):
                return Items.remove_item_from_shop(item_id)

    return False


def add_review_on_item(review):
    if review.writerId is not None and review.itemId is not None and review.description is not None and review.rank is not None:
        purchased_item = PurchasedItems.get_purchased_item_by_user(review.itemId, review.writerId)
        if purchased_item is not False:
            return ReviewsOnItems.add_review_on_item(review) and update_rating(review.itemId, review.rank)
    return False


def edit_shop_item(username, item_id, field_name, new_value):
    item = Items.get_item(item_id)
    result = StoreManagers.get_store_manager(username, item.shop_name)
    if result is not False:
        edit_item_permission = result.permission_edit_item
        if edit_item_permission > 0:
            return Items.update_item(item_id, field_name, new_value)
    else:
        if Owners.get_owner(username, item.shop_name) is not False:
            return Items.update_item(item_id, field_name, new_value)
    return False


def check_in_stock(item_id, amount):
    if item_id is not None and amount is not None and amount > 0:
        item = Items.get_item(item_id)
        if item is not False:
            if item.quantity >= amount:
                return True
    return False


def get_all_purchased_items(username):
    sys_manager = SystemManagers.is_system_manager(username)
    if sys_manager is not False:
        return PurchasedItems.get_all_purchased_items()
    return False


def update_stock(item_id, quantity):
    if item_id is not None and quantity is not None:
        return update_item(item_id, 'quantity', quantity)


def get_item(item_id):
    return Items.get_item(item_id)


def get_item_by_code(code):
    return Items.get_item_by_code(code)


def get_all_reviews_on_item(item_id):
    if item_id is not None:
        item = Items.get_item(item_id)
        if item is not False:
            return ReviewsOnItems.get_all_reviews_on_item(item_id)


def get_item_review_with_writer(item_id, writer_id):
    return ReviewsOnItems.get_reviews_on_item_by_writer(item_id, writer_id)


def update_rating(item_id, rank):
    if item_id is not None and 0 <= int(rank) <= 10:
        sum = Items.get_item(item_id).sum_of_rankings + int(rank)
        num = Items.get_item(item_id).num_of_reviews + 1
        return Items.update_item(item_id, 'sum_of_rankings', sum) and \
               Items.update_item(item_id, 'num_of_reviews', num) and \
               Items.update_item(item_id, 'item_rating', sum / num)


def get_id_by_name(item_name):
    return Items.get_id_by_name(item_name)


def get_item_without_lottery(item_id):
    item = Items.get_item(item_id)
    if item is False or item.kind == "ticket":
        return False
    return item
