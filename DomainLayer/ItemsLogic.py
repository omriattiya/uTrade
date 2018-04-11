from DatabaseLayer import Items, StoreManagers, Shops


def add_item_to_shop(item, shop_id, username):
    if item is not None and shop_id is not None and username is not None:
        manager = StoreManagers.getStoreManager(username, shop_id)
        if manager is not False:
            add_item_permission = manager[2]
            if add_item_permission > 0:
                return Items.add_item_to_shop(item)
    return False


def remove_item_from_shop(item_id, username):
    if item_id is not None:
        item = Items.get_item(item_id)
        manager = StoreManagers.getStoreManager(username, item.shop_id)
        if manager is not False:
            remove_item_permission = manager[3]
            if remove_item_permission > 0:
                return Items.remove_item_from_shop(item_id)
    return False


def add_review_on_item(writer_id, item_id, description, rank):
    if writer_id is not None and item_id is not None and description is not None and rank is not None:
        return Shops.add_review_on_shop(writer_id, item_id, description, rank)


def edit_shop_item(username, item_id, field_name, new_value):
    item = Items.get_item(item_id)
    result = StoreManagers.getStoreManager(username, item.shop_id)
    if result is not False:
        edit_item_permission = result[4]
        if edit_item_permission > 0:
            return Items.updateItem(item_id, field_name, new_value)
    return False


def check_in_stock(item_id, amount):
    if item_id is not None and amount is not None and amount > 0:
        item = Items.get_item(item_id)
        if item is not None:
            if item.quantity >= amount:
                return True
    return False
