from DatabaseLayer import Shops, StoreManagers, PurchasedItems, SystemManagers, Owners, ReviewsOnShops


def create_shop(shop, username):
    if shop is not None and username is not None:
        return Shops.create_shop(shop) and Owners.add_owner(shop.name, username)


def add_review_on_shop(writer_id, shop_name, description, rank):
    if writer_id is not None and shop_name is not None and description is not None and rank is not None:
        return ReviewsOnShops.add_review_on_shop(writer_id, shop_name, description, rank)


def get_shop_purchase_history(username, shop_name):
    manager = StoreManagers.get_store_manager(username, shop_name)
    if manager is not False:
        get_purchase_history_permission = manager[7]
        if get_purchase_history_permission > 0:
            return PurchasedItems.get_purchased_items_by_shop(shop_name)
    return False


def close_shop_permanently(username, shop_name):
    if username is not None and shop_name is not None:
        sys_manager = SystemManagers.is_system_manager(username)
        if sys_manager is not False:
            return Shops.close_shop_permanently(shop_name)
        return False
    return False
