from DatabaseLayer import Items,StoreManagers


def add_item_to_shop(item, shop_id):
    if item is not None and shop_id is not None:
        return Items.add_item_to_shop(item)


def remove_item_from_shop(item_id):
    if item_id is not None:
        return Items.remove_item_from_shop(item_id)


def add_review_on_item(writer_id, item_id, description, rank):
    if writer_id is not None and item_id is not None and description is not None and rank is not None:
        return Items.add_review_on_shop(writer_id, item_id, description, rank)


def edit_item(username, item_id, field_name, new_value):
    result = StoreManagers.getStoreManager(username)
    if result is not False:
        edit_item_permission = result[3]
        if edit_item_permission > 0:
            return Items.updateItem(item_id,field_name,new_value)
    return False