from sqlite3 import Error

from DatabaseLayer.getConn import commit_command, select_command, get_conn
from SharedClasses.Item import Item


def fetch_items(items):
    items_arr = []
    for item in items:
        items_arr.append(Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                              item[10], item[11]))
    return items_arr


def fetch_item(item):
    if len(item) == 0:
        return False
    item = item[0]
    item = Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                item[10], item[11])
    return item


def get_item(item_id):
    sql_query = """
                SELECT *
                FROM Items
                Where id = '{}'
            """.format(item_id)
    return fetch_item(select_command(sql_query))


def search_items_by_name(item_name):
    sql_query = """
                SELECT *
                FROM Items,Shops
                WHERE Items.name = '{}' AND
                Shops.status = 'Active' AND
                Items.shop_name = Shops.name AND Items.kind <> 'prize'
              """.format(item_name)
    return fetch_items(select_command(sql_query))


def add_item_to_shop(item):
    sql_query = """
                    INSERT INTO Items (shop_name, name, category, keyWords, price, quantity, kind, url , item_rating,
                      sum_of_rankings, num_of_reviews)  
                    VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}');
                  """.format(item.shop_name,
                             item.name, item.category,
                             item.keyWords,
                             item.price, item.quantity, item.kind, item.url, 5, 0, 0)
    return commit_command(sql_query)


def add_item_to_shop_and_return_id(item):
    sql_query = """
                INSERT INTO Items (shop_name, name, category, keyWords, price, quantity, kind, url , item_rating,
                  sum_of_rankings, num_of_reviews)  
                VALUES ('{}', '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}');
              """.format(item.shop_name,
                         item.name, item.category,
                         item.keyWords,
                         item.price, item.quantity, item.kind, item.url, 5, 0, 0)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(sql_query)
        conn.commit()
        to_return = c.lastrowid
        conn.close()
        return to_return
    except Error as e:
        return False


def remove_item_from_shop(item_id):
    sql_query = """
                DELETE FROM Items
                WHERE id = '{}'
              """.format(item_id)
    return commit_command(sql_query)


def search_item_in_shop(shop_name, item_name):
    sql_query = """
                SELECT *
                FROM Items,Shops
                WHERE Items.name = '{}'  AND Shops.name = '{}' AND Items.shop_name = '{}' AND Items.kind <> 'prize'
              """.format(item_name, shop_name, shop_name)
    return fetch_item(select_command(sql_query))


def search_items_in_shop(shop_name):
    sql_query = """
                SELECT *
                FROM Items,Shops
                WHERE Shops.name = Items.shop_name AND Items.shop_name = '{}' AND Items.kind <> 'prize'
              """.format(shop_name)
    return fetch_items(select_command(sql_query))


def search_items_by_category(item_category):
    sql_query = """
                SELECT *
                FROM Items,Shops
                WHERE category = '{}' AND Shops.status = 'Active' AND Shops.name = Items.shop_name AND Items.kind <> 'prize'
              """.format(item_category)
    return fetch_items(select_command(sql_query))


def search_items_by_keywords(item_keyword):
    sql_query = """
                SELECT *
                FROM Items,Shops
                WHERE keyWords = '{}' AND Shops.status = 'Active' AND Shops.name = Items.shop_name AND Items.kind <> 'prize'
              """.format(item_keyword)
    return fetch_items(select_command(sql_query))


def update_item(item_id, field_name, new_value):
    sql = """
            UPDATE Items
            SET {} = '{}'
            WHERE id = '{}'
            """.format(field_name, new_value, item_id)
    return commit_command(sql)


def get_shop_items(shop_name):
    sql = """
            SELECT * FROM Items WHERE shop_name='{}'
            """.format(shop_name)
    return fetch_items(select_command(sql))


def get_item_by_code(code):
    sql_query = """
                SELECT Items.*
                FROM Items,InvisibleDiscounts
                WHERE Items.id = InvisibleDiscounts.item_id AND InvisibleDiscounts.code = '{}'
                """.format(code)
    return fetch_item(select_command(sql_query))


def get_top_five_ranked_items():
    sql = """
            SELECT Items.* FROM Items,Shops 
            WHERE Items.kind <> 'prize' AND Items.shop_name = Shops.name AND Shops.status = 'Active'
            ORDER BY item_rating DESC limit 5
            """
    return fetch_items(select_command(sql))


def get_id_by_name(item_name):
    sql = """
                SELECT id FROM Items
                WHERE name = '{}'
                """.format(item_name)
    return select_command(sql)[0][0]
