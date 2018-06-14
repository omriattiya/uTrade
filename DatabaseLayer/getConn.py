import datetime
import sqlite3
from sqlite3 import Error

from django.db import connection

from DatabaseLayer import initializeDatabase
from SharedClasses.LogTuple import ErrorTuple


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
        add_error_log(ErrorTuple("DB ERROR", now_time(), "COMMIT COMMAND", str(e)))
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
        add_error_log(ErrorTuple("DB ERROR", now_time(), "SELECT COMMAND", str(e)))
        conn.close()
        return []


def add_error_log(tuple_log):
    sql_query = """
            INSERT INTO ErrorLogs (username, time, event, additional_details)  
            VALUES ('{}', '{}', '{}', '{}');
          """.format(tuple_log.username, tuple_log.time, tuple_log.event, tuple_log.additional_details)
    return commit_command(sql_query)


def now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
