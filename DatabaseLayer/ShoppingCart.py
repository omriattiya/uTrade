import sqlite3

conn = sqlite3.connect('../db.sqlite3')


def add_item_to_cart(user_id, item_id, quantity):
    c = conn.cursor()
    c.execute("""
                INSERT INTO ShoppingCartItems (userID, itemID, quantity) 
                VALUES ({},{},{})
              """.format(user_id, item_id, quantity))
    return c.fetchall()

