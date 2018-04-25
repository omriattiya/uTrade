from DatabaseLayer import Items, Shops
import enchant


def search_by_name(item_name):
    if item_name is not None:
        return Items.search_items_by_name(item_name)
    else:
        return False


def search_shop(shop_name):
    if shop_name is not None:
        return Shops.search_shop(shop_name)


def search_item_in_shop(shop_name, item_name):
    if item_name is not None:
        if shop_name is not None:
            return Items.search_item_in_shop(shop_name, item_name)
    else:
        return False


def search_items_in_shop(shop_name):
    if shop_name is not None:
        return Items.search_items_in_shop(shop_name)
    else:
        return False


def search_by_category(item_category):
    if item_category is not None:
        return Items.search_items_by_category(item_category)


def search_by_keywords(item_keywords):
    if item_keywords is not None:
        keywords_array = item_keywords.replace(';', ' ')
        return Items.search_items_by_keywords(keywords_array)


def get_similar_words(word):
    d = enchant.Dict()
    return d.suggest(word)
