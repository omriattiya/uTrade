from DatabaseLayer import Items, StoreManagers, Shops, Owners, SystemManagers


def add_item_to_shop(item, username):
    if item is not None and item.shop_name is not None and username is not None:
        is_manager = StoreManagers.get_store_manager(username, item.shop_name)
        if is_manager is not False:
            add_item_permission = is_manager[2]
            if add_item_permission > 0:
                return Items.add_item_to_shop(item)
        if Owners.get_owner(username, item.shop_name) is not False:
            return Items.add_item_to_shop(item)
    return False


def remove_item_from_shop(item_id, username):
    if item_id is not None:
        item = Items.get_item(item_id)
        manager = StoreManagers.get_store_manager(username, item.shop_name)
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
    result = StoreManagers.get_store_manager(username, item.shop_name)
    if result is not False:
        edit_item_permission = result[4]
        if edit_item_permission > 0:
            return Items.update_item(item_id, field_name, new_value)
    return False


def check_in_stock(item_id, amount):
    if item_id is not None and amount is not None and amount > 0:
        item = Items.get_item(item_id)
        if item is not None:
            if item.quantity >= amount:
                return True
    return False


def get_all_purchased_items(username):
    sys_manager = SystemManagers.is_system_manager(username)
    if sys_manager is not False:
        return Items.get_all_purchased_items()
    return False

