from DatabaseLayer import Items


def search_by_name(item_name):
    if item_name is not None:
        return Items.searchItemsByName(item_name)


def search_by_category(item_category):
    if item_category is not None:
        return Items.searchItemsByCategory(item_category)


def search_by_keywords(item_keywords):
    if item_keywords is not None:
        keywords_array = item_keywords.split(';')
        items_with_all_keywords = Items.searchItemsByCategory(keywords_array[0])
        for keyword in keywords_array:
            items_with_all_keywords = items_with_all_keywords.intersection(Items.searchItemsByCategory(keyword))
        return items_with_all_keywords
