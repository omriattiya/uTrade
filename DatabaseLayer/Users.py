import sqlite3

conn = sqlite3.connect('../db.sqlite3')


def remove_user(registered_user):
    c = conn.cursor()
    c.execute("""
                DELETE FROM Users
                WHERE username = {}
              """.format(registered_user))
    return c.fetchall()
