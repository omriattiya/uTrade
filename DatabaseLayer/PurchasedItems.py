from SharedClasses.Item import Item
from DatabaseLayer.getConn import select_command, commit_command


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
            'purchased_item': {item[8: len(item)]}})

    return list_of_items


def get_all_purchased_items():
    sql_query = """
                SELECT *
               FROM Items
              """
    items = select_command(sql_query)
    list_of_items = []
    for item in items:
        list_of_items.append({
            'item': Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6]),
            'purchased_item': {item[8: len(item)]}})

    return list_of_items


def add_purchased_item(purchased_item, purchase_date, quantity, price, user_id):
    sql_query = """
                INSERT INTO PurchasedItems(PurchasedItem, purchaseDate,quantity,price, username)
                VALUES ('{}','{}','{}','{}','{}')
                """.format(purchased_item, purchase_date, quantity, price, user_id)
    return commit_command(sql_query)


def get_purchased_item(item_id):
    sql_query = """
                    SELECT *
                    FROM PurchasedItems
                    WHERE PurchasedItem = '{}'
                """.format(item_id)
    return select_command(sql_query)
