import sqlite3
from sqlite3 import Error


def get_conn():
    conn = sqlite3.connect('db.sqlite3')
    conn.execute("""
                      PRAGMA foreign_keys = ON
              """)
    return conn

def commit_command(sql_query):
    try:
        conn = get_conn()
        conn.cursor().execute(sql_query)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        return False


def select_command(sql_query):
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(sql_query)
        results = c.fetchall()
        conn.close()
        return results
    except Error as e:
        return False
