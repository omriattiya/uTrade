from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.ShoppingCart import ShoppingCart


def parse_shopping_carts(shopping_carts):
    shopping_carts_list = []
    for shopping_cart in shopping_carts:
        shopping_carts_list.append(ShoppingCart(shopping_cart[0], shopping_cart[1], shopping_cart[2]))
    return shopping_carts_list


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

    shop_carts_items = select_command(sql_query)
    shop_carts_items = parse_shopping_carts(shop_carts_items)
    if len(shop_carts_items) == 0:
        return False
    return shop_carts_items


def check_empty(username):
    sql_query = """
                SELECT *
                FROM ShoppingCart
                WHERE userName = '{}'
              """.format(username)
    items = select_command(sql_query)
    return len(items) == 0
