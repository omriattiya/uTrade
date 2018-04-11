from SharedClasses.Item import Item
from DatabaseLayer.getConn import select_command


def get_purchased_items_by_shop(shop_name):
    sql_query = """
                SELECT Items.*, PurchasedItems.*
                FROM PurchasedItems, Items, Shops
                WHERE Items.shop_name = '{}' AND PurchasedItems.PurchasedItem = Items.id
            """.format(shop_name)
    items = select_command(sql_query)
    list_of_items = []
    for item in items:
        list_of_items.append({
            'item': Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6]),
            'purchased_item': {item[8 : len(item)]}})

    return list_of_items

