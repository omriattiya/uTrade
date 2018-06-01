import enchant

from DatabaseLayer import Items, Shops


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
        matched_items = []
        splitted_keywords = item_keywords.split()
        for keyword in splitted_keywords:
            matched_items.append(Items.search_items_by_keywords(keyword))
        seen = set()
        set_to_return = []
        for my_list in matched_items:
            for obj in my_list:
                if obj.id not in seen:
                    set_to_return.append(obj)
                    seen.add(obj.id)
        return set_to_return


def get_similar_words(word):
    d = enchant.Dict("en_US")
    return d.suggest(word)
