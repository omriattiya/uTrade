from DatabaseLayer.getConn import select_command, commit_command
from SharedClasses.PurchasedItem import PurchasedItem


def fetch_purchased_items(results):
    array = []
    for item in results:
        array.append(PurchasedItem(item[0], item[1], item[2], item[3]))
    return array


def fetch_purchased_item(result):
    if len(result) == 0:
        return False
    result = result[0]
    return PurchasedItem(result[0], result[1], result[2], result[3])


def get_purchased_items_by_shop(shop_name):
    sql_query = """
                SELECT PurchasedItems.*
                FROM PurchasedItems, Items, Shops
                WHERE Items.shop_name = '{}' AND PurchasedItems.PurchasedItem = Items.id AND Shops.name = Items.shop_name
            """.format(shop_name)
    return fetch_purchased_items(select_command(sql_query))


def get_purchased_items_by_purchase(purchase_id):
    sql_query = """
                    SELECT *
                    FROM PurchasedItems
                    WHERE purchaseId = '{}'
                """.format(purchase_id)
    return fetch_purchased_items(select_command(sql_query))


def get_all_purchased_items():
    sql_query = """
                SELECT *
               FROM PurchasedItems
              """
    return fetch_purchased_items(select_command(sql_query))


def add_purchased_item(purchase_id, purchase_item, quantity, price):
    sql_query = """
                INSERT INTO PurchasedItems(purchaseId,purchasedItem,quantity,price)
                VALUES ('{}','{}','{}','{}')
                """.format(purchase_id, purchase_item, quantity, price)
    return commit_command(sql_query)


def get_purchased_item(item_id):
    sql_query = """
                    SELECT *
                    FROM PurchasedItems
                    WHERE PurchasedItem = {}
                """.format(item_id)
    return fetch_purchased_item(select_command(sql_query))


def get_purchased_item_by_user(item_id, username):
    sql_query = """
                        SELECT PurchasedItems.*
                        FROM PurchasedItems,Purchases
                        WHERE PurchasedItems.purchasedItem = {} AND PurchasedItems.purchaseId = Purchases.purchaseId AND Purchases.username = '{}'
                    """.format(item_id,username)
    return fetch_purchased_item(select_command(sql_query))


def get_purchased_item_by_shop_and_username(shop_name, username):
    sql_query = """
                SELECT PurchasedItems.*
                FROM PurchasedItems, Items, Purchases
                WHERE Items.shop_name = '{}' AND PurchasedItems.purchasedItem = Items.id AND Purchases.purchaseId = PurchasedItems.purchaseId AND Purchases.username='{}'
            """.format(shop_name,username)
    return fetch_purchased_item(select_command(sql_query))