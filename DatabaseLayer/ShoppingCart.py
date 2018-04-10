from sqlite3 import Error

from DatabaseLayer.getConn import getConn


def remove_item_shopping_cart(username, item_id):
    c = getConn().cursor()
    c.execute("""
                DELETE FROM ShoppingCart
                WHERE userName = {} AND itemId = {}
              """.format(username, item_id))
    return c.fetchall()


def browse_shopping_cart(username):
    c = getConn().cursor()
    c.execute("""
                SELECT *
                FROM ShoppingCart
                WHERE userName = {}
              """.format(username))
    return c.fetchall()


def add_item(user_id, item_id, quantity):
    conn = getConn()
    c = conn.cursor()

    c.execute("""
                INSERT INTO ShoppingCart (userName, itemId, itemQuantity) 
                VALUES ({},{},{})
              """.format(user_id, item_id, quantity))
    try:
        conn.commit()
        conn.close()
        return True
    except Error as e:
        return False

