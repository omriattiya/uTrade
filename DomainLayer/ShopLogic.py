from DatabaseLayer import Shops, StoreManagers, PurchasedItems


def create_shop(shop, user_id):
    if shop is not None and user_id is not None:
        Shops.create_shop(shop)
        Shops.connect_shop_to_owner(user_id, shop)
        return True


def add_review_on_shop(writer_id, shop_id, description, rank):
    if writer_id is not None and shop_id is not None and description is not None and rank is not None:
        return Shops.add_review_on_shop(writer_id, shop_id, description, rank)


def get_shop_purchase_history(username, shop_id):
    manager = StoreManagers.getStoreManager(username, shop_id)
    if manager is not False:
        get_purchase_history_permission = manager[7]
        if get_purchase_history_permission > 0:
            return PurchasedItems.get_purchased_items_by_shop(shop_id)
    return False
