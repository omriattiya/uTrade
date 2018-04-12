from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.Item import Item


def fetch_items(items):
    items_arr = []
    for item in items:
        items_arr.append(Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6]))
    return items_arr


def fetch_item(item):
    if len(item) == 0:
        return False
    item = item[0]
    item = Item(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
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
                FROM Items
                WHERE name = '{}'
              """.format(item_name)
    return fetch_items(select_command(sql_query))


def add_item_to_shop(item):
    sql_query = """
                INSERT INTO Items (shop_name, name, category, keyWords, price, quantity)  
                VALUES ('{}', '{}', '{}', '{}', {}, {});
              """.format(item.shop_name,
                         item.name, item.category,
                         item.keyWords,
                         item.price, item.quantity)
    return commit_command(sql_query)


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
                WHERE Items.name = '{}'  AND Shops.name = '{}' AND Items.shop_name = '{}'
              """.format(item_name, shop_name, shop_name)
    return fetch_item(select_command(sql_query))


def search_items_by_category(item_category):
    sql_query = """
                SELECT *
                FROM Items
                WHERE category = '{}'
              """.format(item_category)
    return fetch_items(select_command(sql_query))


def search_items_by_keywords(item_keyword):
    sql_query = """
                SELECT *
                FROM Items
                WHERE keyWords = '{}'
              """.format(item_keyword)
    return fetch_items(select_command(sql_query))


def update_item(item_id, field_name, new_value):
    sql = """
            UPDATE Items
            SET {} = '{}'
            WHERE id = '{}'
            """.format(field_name, new_value, item_id)
    return commit_command(sql)
