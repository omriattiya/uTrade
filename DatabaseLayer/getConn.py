import sqlite3


def getConn():
    return sqlite3.connect('db.sqlite3')
