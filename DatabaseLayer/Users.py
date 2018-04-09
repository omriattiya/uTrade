import sqlite3

conn = sqlite3.connect('../db.sqlite3')


def remove_user(username):
    c = conn.cursor()
    c.execute("""
                DELETE FROM Users
                WHERE username = {}
              """.format(username))
    return c.fetchall()
