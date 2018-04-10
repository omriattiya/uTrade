from DatabaseLayer import Items


def add_item_to_shop(item, shop_id):
    if item is not None and shop_id is not None:
        return Items.add_item_to_shop(item)


def remove_item_from_shop(item_id):
    if item_id is not None:
        return Items.remove_item_from_shop(item_id)


def add_review_on_item(writer_id, item_id, description, rank):
    if writer_id is not None and item_id is not None and description is not None and rank is not None:
        return Items.add_review_on_shop(writer_id, item_id, description, rank)
