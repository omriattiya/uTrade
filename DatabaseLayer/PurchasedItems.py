from DatabaseLayer.getConn import select_command, commit_command
from SharedClasses.PurchasedItem import PurchasedItem


def fetch_purchased_items(results):
    array = []
    for item in results:
        array.append(PurchasedItem(item[0], item[1], item[2], item[3], item[4], item[5]))
    return array


def fetch_purchased_item(result):
    if len(result) == 0:
        return False
    result = result[0]
    return PurchasedItem(result[0], result[1], result[2], result[3], result[4], result[5])


def get_purchased_items_by_shop(shop_name):
    sql_query = """
                SELECT PurchasedItems.*
                FROM PurchasedItems, Items, Shops
                WHERE Items.shop_name = '{}' AND PurchasedItems.PurchasedItem = Items.id AND Shops.name = Items.shop_name
            """.format(shop_name)
    return fetch_purchased_items(select_command(sql_query))


def get_all_purchased_items():
    sql_query = """
                SELECT *
               FROM PurchasedItems
              """
    return fetch_purchased_items(select_command(sql_query))


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
    return fetch_purchased_item(select_command(sql_query))
