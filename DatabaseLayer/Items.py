import sqlite3

conn = sqlite3.connect('../db.sqlite3')


def searchItemsByName(item_name):
    c = conn.cursor()
    c.execute("""
                SELECT *
                FROM Items
                WHERE name = {}
              """.format(item_name))
    return c.fetchall()
