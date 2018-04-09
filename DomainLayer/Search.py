from DatabaseLayer import Items


def search_by_name(item_name):
    if item_name is not None:
        return Items.searchItemsByName(item_name)

