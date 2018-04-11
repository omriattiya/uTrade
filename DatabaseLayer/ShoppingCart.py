from DatabaseLayer.getConn import commit_command, select_command


def remove_item_shopping_cart(username, item_id):
    sql_query = """
                DELETE FROM ShoppingCart
                WHERE userName = '{}' AND itemId = '{}'
              """.format(username, item_id)
    return commit_command(sql_query)


def add_item_shopping_cart(username, item_id, quantity):
    sql = """
                INSERT INTO ShoppingCart (userName, itemId, itemQuantity) 
                VALUES ('{}','{}','{}')
              """.format(username, item_id, quantity)
    return commit_command(sql)


def get_cart_items(username):
    sql_query = """
        SELECT * FROM ShoppingCart WHERE userName LIKE '{}'
    """.format(username)
    return select_command(sql_query)


def check_empty(username):
    sql_query = """
                SELECT *
                FROM ShoppingCart
                WHERE userName = '{}'
              """.format(username)
    items = select_command(sql_query)
    return len(items) == 0
