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
        totalsum = list()
        for keyword in keywords_array:
            currentsum = list()
            items_with_current_keyword = (Items.search_items_by_keywords(keyword))
            for x in items_with_current_keyword:
                currentsum.append(x[2])
            totalsum.append(currentsum)
        totalsum = totalsum[0]
        aftherset = set()
        for item in totalsum:
            aftherset.add(item)
        to_return_array = []
        for item in aftherset:
            to_return_array = to_return_array + search_by_name(item)
        return to_return_array
