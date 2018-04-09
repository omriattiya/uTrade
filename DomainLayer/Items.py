from DatabaseLayer import Items


def add_item_to_shop(item, shop_id):
    if item is not None and shop_id is not None:
        return Items.add_item_to_shop(item)


def remove_item_from_shop(item_id):
    if item_id is not None:
        return Items.remove_item_from_shop(item_id)
