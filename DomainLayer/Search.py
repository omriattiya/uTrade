from DatabaseLayer import Items, Shops


def search_by_name(item_name):
    if item_name is not None:
        return Items.searchItemsByName(item_name)


def search_shop(shop_name):
    if shop_name is not None:
        return Shops.searchShop(shop_name)


def search_item_in_shop(shop_name, item_name):
    if item_name is not None:
        if shop_name is not None:
            return Items.searchItemInShop(shop_name, item_name)
