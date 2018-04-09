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

def add_item_to_shop(item):
    c = conn.cursor()
    c.execute("""
                INSERT INTO Items [(id, shopid, name,
                 category, keyWords,
                  rank, price, quantity)]  
VALUES ({}, {}, {}, {}, {}, {}, {}, {});
              """.format(item.id, item.shop_id,
                         item.name, item.category,
                         item.keyWords, item.rank,
                         item.price, item.quantity))
    return c.fetchall()


def remove_item_from_shop(item_id):
    c = conn.cursor()
    c.execute("""
                DELETE FROM Items
                WHERE id = {}
              """.format(item_id))
    return c.fetchall()
