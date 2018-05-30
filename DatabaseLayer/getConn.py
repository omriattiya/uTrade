import sqlite3
from sqlite3 import Error
from django.db import connection


def get_conn():
    conn = sqlite3.connect('db.sqlite3')
    conn.execute("""
                      PRAGMA foreign_keys = ON
              """)
    return conn
    # return connection


def commit_command(sql_query):
    conn = get_conn()
    try:
        conn.cursor().execute(sql_query)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        conn.close()
        return False


def select_command(sql_query):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute(sql_query)
        results = c.fetchall()
        conn.close()
        return results
    except Error as e:
        conn.close()
        return []
