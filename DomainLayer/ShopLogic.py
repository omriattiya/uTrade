from DatabaseLayer import Items
from DatabaseLayer import Shops, StoreManagers, PurchasedItems, SystemManagers, Owners, ReviewsOnShops
from DatabaseLayer.PurchasedItems import get_purchased_item_by_shop_and_username
from DomainLayer import LoggerLogic
from DomainLayer.SearchLogic import search_shop
from SharedClasses.Owner import Owner


def create_shop(shop, username):
    if shop is not None and username is not None:
        if Shops.search_shop(shop.name) is False:
            if Shops.create_shop(shop):
                if Owners.add_owner(Owner(username, shop.name, None)):
                    LoggerLogic.add_event_log(username, "OPEN SHOP")
                    return "SUCCESS"
                return "FAILED: Adding Owner"
            return "FAILED: Adding Shop"
        return "FAILED: Shop name is taken"
    return "FAILED: Missing parameters"


def add_review_on_shop(shop_review):
    if shop_review.writerId is not None and shop_review.shop_name is not None \
            and shop_review.description is not None and shop_review.rank is not None:
        purchased_item = get_purchased_item_by_shop_and_username(shop_review.shop_name, shop_review.writerId)
        if purchased_item is not False:
            return ReviewsOnShops.add_review_on_shop(shop_review)
        return False


def get_shop_purchase_history(username, shop_name):
    manager = StoreManagers.get_store_manager(username, shop_name)
    owner = Owners.get_owner(username, shop_name)
    if manager is not False:
        if manager.permission_get_purchased_history > 0:
            return PurchasedItems.get_purchased_items_by_shop(shop_name)
    else:
        if owner is not False:
            return PurchasedItems.get_purchased_items_by_shop(shop_name)
    return False


def close_shop_permanently(username, shop_name):
    if username is not None and shop_name is not None:
        sys_manager = SystemManagers.is_system_manager(username)
        if sys_manager is not False:
            shop = search_shop(shop_name)
            if shop is not False:
                return Shops.close_shop_permanently(shop_name)
        return False
    return False


def get_shop_items(shop_name):
    return Items.get_shop_items(shop_name=shop_name)


def get_shop_reviews(shop_name):
    return ReviewsOnShops.get_all_reviews_on_shop(shop_name)


def get_shop_rank(shop_name):
    return ReviewsOnShops.get_shop_rank(shop_name)


def get_store_managers(shop_name):
    return StoreManagers.get_store_managers_on_shop(shop_name)


def get_all_shops():
    return Shops.get_all_shops()


def get_store_owners(shop_name):
    return Owners.get_owners_by_shop(shop_name)