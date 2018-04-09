import sqlite3
from sqlite3 import Error


def connectToDatabase(databasePath):
    try:
        conn = sqlite3.connect(databasePath)
        return conn
    except Error as e:
        print(e)
        pass


def initTables(conn, tables):
    c = conn.cursor()
    for table in tables:
        c.execute(table)
    pass


def init(databasePath, tables):
    conn = connectToDatabase(databasePath)
    if conn is not None:
        initTables(conn, tables)


tables_sql = [
    """CREATE TABLE IF NOT EXISTS RegisteredUsers(
        username CHAR(30) PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'Customer'
    )""",

    """CREATE TABLE IF NOT EXISTS Items(
        id INTEGER PRIMARY KEY,
        shopId INTEGER REFERENCES Shops(id),
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        keyWords TEXT,
        rank INTEGER,
        price REAL NOT NULL,
        quantity INTEGER
    )""",
    """
        CREATE TABLE IF NOT EXISTS Shops(
          id INTEGER PRIMARY KEY,
          title CHAR(30) NOT NULL,
          rank REAL,
          status TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Reviews(
          reviewId INTEGER PRIMARY KEY ,
          writerId INTEGER REFERENCES RegisteredUsers(username),
          shopId INTEGER REFERENCES Shops(id),
          description TEXT,
          rank INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS PurchasedItems(
          purchaseId INTEGER PRIMARY KEY,
          PurchasedItem INTEGER REFERENCES Items(id),
          purchasedData TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingCartItems(
          userID CHAR(30) REFERENCES RegisteredUsers(username),
          itemID INTEGER REFERENCES Items(id),
          quantity INTEGER,
          PRIMARY KEY(userID, itemID) 
        )
    """
]

init('../db.sqlite3', tables_sql)
