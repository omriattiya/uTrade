from DatabaseLayer import Shops, StoreManagers, PurchasedItems, SystemManagers, Owners, ReviewsOnShops, Items
from DomainLayer.SearchLogic import search_shop
from DomainLayer.UsersLogic import get_purchase_history
from SharedClasses.Owner import Owner


def create_shop(shop, username):
    if shop is not None and username is not None:
        if Shops.search_shop(shop.name) is False:
            return Shops.create_shop(shop) and Owners.add_owner(Owner(username, shop.name, None))
    return False


def add_review_on_shop(shop_review):
    if shop_review.writerId is not None and shop_review.shop_name is not None \
            and shop_review.description is not None and shop_review.rank is not None:

        history = get_purchase_history(shop_review.writerId)
        is_found = False
        for item in history:
            if item.username == shop_review.writerId:
                is_found = True
        if is_found:
            return ReviewsOnShops.add_review_on_shop(shop_review)
        return False


def get_shop_purchase_history(username, shop_name):
    manager = StoreManagers.get_store_manager(username, shop_name)
    if manager is not False:
        if manager.permission_get_purchased_history > 0:
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