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


def searchItemsByCategory(item_category):
    c = conn.cursor()
    c.execute("""
                SELECT *
                FROM Items
                WHERE name = {}
              """.format(item_category))
    return c.fetchall()


def searchItemsByKeywords(item_keyword):
    c = conn.cursor()
    c.execute("""
                SELECT *
                FROM Items
                WHERE name = {}
              """.format(item_keyword))
    return c.fetchall()
