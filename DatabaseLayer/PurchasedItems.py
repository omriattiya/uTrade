from SharedClasses.Item import Item
from DatabaseLayer.getConn import get_conn, commit_command
from sqlite3 import Error


def get_purchased_items_by_shop(shop_id):
    conn = get_conn()
    sql = """
                SELECT Items.*, PurchasedItems.*
                FROM PurchasedItems, Items, Shops
                WHERE Items.shopId = '{}' AND PurchasedItems.PurchasedItem = Items.id
            """.format(shop_id)
    try:
        c = conn.cursor()
        c.execute(sql)
        items = c.fetchall()
        list_of_items = []
        for item in items:
            list_of_items.append({
                'item': Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]),
                'purchased_item': {item[8], len(item)}})

        return list_of_items
    except Error as e:
        return False
