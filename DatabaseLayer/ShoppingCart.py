from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.ShoppingCart import ShoppingCart


def fetch_cart_item(cart_item):
    if len(cart_item) == 0:
        return False
    cart_item = cart_item[0]
    cart_item = ShoppingCart(cart_item[0], cart_item[1], cart_item[2], cart_item[3])
    return cart_item


def parse_shopping_carts(shopping_carts):
    shopping_carts_list = []
    for shopping_cart in shopping_carts:
        shopping_carts_list.append(ShoppingCart(shopping_cart[0], shopping_cart[1], shopping_cart[2], shopping_cart[3]))
    return shopping_carts_list


def remove_item_shopping_cart(username, item_id):
    sql_query = """
                DELETE FROM ShoppingCart
                WHERE userName = '{}' AND itemId = {}
              """.format(username, item_id)
    return commit_command(sql_query)


def add_item_shopping_cart(shop_cart):
    sql = """
                INSERT INTO ShoppingCart (userName, itemId, itemQuantity) 
                VALUES ('{}',{},{})
              """.format(shop_cart.username, shop_cart.item_id, shop_cart.item_quantity)
    return commit_command(sql)


def get_shopping_cart_item(shop_cart):
    sql = """
            SELECT * FROM ShoppingCart WHERE username = '{}' AND itemID = {}
            """.format(shop_cart.username, shop_cart.item_id)
    return fetch_cart_item(select_command(sql))


def update_item_shopping_cart(username, item_id, new_quantity):
    sql = """
            UPDATE ShoppingCart
            SET itemQuantity = '{}'
            WHERE username = '{}' AND itemId = {}
              """.format(new_quantity, username, item_id)
    return commit_command(sql)


def update_code_shopping_cart(username, item_id, code):
    sql = """
            UPDATE ShoppingCart
            SET code = '{}'
            WHERE username = '{}' AND itemId = {}
              """.format(code, username, item_id)
    return commit_command(sql)


def get_cart_items(username):
    sql_query = """
        SELECT * FROM ShoppingCart WHERE userName LIKE '{}'
    """.format(username)

    shop_carts_items = select_command(sql_query)
    shop_carts_items = parse_shopping_carts(shop_carts_items)
    return shop_carts_items


def check_empty(username):
    sql_query = """
                SELECT *
                FROM ShoppingCart
                WHERE userName = '{}'
              """.format(username)
    items = select_command(sql_query)
    return len(items) == 0
