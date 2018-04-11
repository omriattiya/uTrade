from DatabaseLayer import Shops, StoreManagers, PurchasedItems, SystemManagers, Owners


def create_shop(shop, user):
    if shop is not None and user is not None:
        return Shops.create_shop(shop) and Owners.add_owner(user, shop)


def add_review_on_shop(writer_id, shop_name, description, rank):
    if writer_id is not None and shop_name is not None and description is not None and rank is not None:
        return Shops.add_review_on_shop(writer_id, shop_name, description, rank)


def search_shop_purchase_history(username, shop_name):
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
