import sqlite3
from sqlite3 import Error


def get_conn():
    return sqlite3.connect('db.sqlite3')


def commit_command(sql_query):
    try:
        conn = get_conn()
        conn.cursor().execute(sql_query)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        return False
