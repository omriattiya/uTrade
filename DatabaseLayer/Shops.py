import sqlite3

conn = sqlite3.connect('../db.sqlite3')


def searchShop(shop_name):
    c = conn.cursor()
    c.execute("""
                SELECT *
                FROM Shops
                WHERE title = {}
              """.format(shop_name))
    return c.fetchall()