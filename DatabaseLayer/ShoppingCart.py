from DatabaseLayer.getConn import get_conn, commit_command


# TODO: c = get_conn() and CLOSE THE CONNECTION!!
def remove_item_shopping_cart(username, item_id):
    c = get_conn().cursor()
    c.execute("""
                DELETE FROM ShoppingCart
                WHERE userName = '{}' AND itemId = '{}'
              """.format(username, item_id))
    return c.fetchall()


# TODO: c = get_conn() and CLOSE THE CONNECTION!!
def browse_shopping_cart(username):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM ShoppingCart
                WHERE userName = '{}'
              """.format(username))
    return c.fetchall()


def add_item_shopping_cart(user_id, item_id, quantity):
    sql = """
                INSERT INTO ShoppingCart (userName, itemId, itemQuantity) 
                VALUES ('{}','{}','{}')
              """.format(user_id, item_id, quantity)
    return commit_command(sql)


def get_cart_items(user_id):
    conn = get_conn()
    c = conn.cursor()
    sql = """
        SELECT * FROM ShoppingCart WHERE userName LIKE '{}'
    """.format(user_id)
    c.execute(sql)
    results = c.fetchall()
    conn.close()
    return results
