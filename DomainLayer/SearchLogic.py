from DatabaseLayer import Items,Shops


def search_by_name(item_name):
    if item_name is not None:
        return Items.search_items_by_name(item_name)


def search_shop(shop_name):
    if shop_name is not None:
        return Shops.search_shop(shop_name)


def search_item_in_shop(shop_name, item_name):
    if item_name is not None:
        if shop_name is not None:
            return Items.search_item_in_shop(shop_name, item_name)


def search_by_category(item_category):
    if item_category is not None:
        return Items.search_items_by_category(item_category)


def search_by_keywords(item_keywords):
    if item_keywords is not None:
        keywords_array = item_keywords.split(';')
        items_with_all_keywords = Items.search_items_by_category(keywords_array[0])
        for keyword in keywords_array:
            items_with_all_keywords = items_with_all_keywords.intersection(Items.search_items_by_category(keyword))
        return items_with_all_keywords
