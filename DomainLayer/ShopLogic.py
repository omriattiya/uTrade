from DatabaseLayer import Shops, StoreManagers, PurchasedItems, SystemManagers, Owners


def create_shop(shop, user_id):
    if shop is not None and user_id is not None:
        return Shops.create_shop(shop) and Owners.add_owner(shop.id, user_id)


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


def close_shop_permanently(username, shop_id):
    if username is not None and shop_id is not None:
        sys_manager = SystemManagers.is_system_manager(username)
        if sys_manager is not False:
            return Shops.close_shop_permanently(shop_id)
        return False
    return False
