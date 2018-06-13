import sqlite3
from sqlite3 import Error

from django.db import connection

from DatabaseLayer import initializeDatabase
from DomainLayer import LoggerLogic


def get_conn():
    if initializeDatabase.is_test:
        conn = sqlite3.connect('db.sqlite3')
        conn.execute("""
                              PRAGMA foreign_keys = ON
                      """)
        return conn
    else:
        return connection


def commit_command(sql_query):
    conn = get_conn()
    try:
        conn.cursor().execute(sql_query)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        LoggerLogic.add_error_log("DB ERROR", "COMMIT COMMAND", str(e))
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
        print(e)
        LoggerLogic.add_error_log("DB ERROR", "SELECT COMMAND", str(e))
        conn.close()
        return []
