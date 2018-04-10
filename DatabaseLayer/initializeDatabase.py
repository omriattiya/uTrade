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
    try:
        for table in tables:
            c.execute(table)
    except Error as e:
        print(e)


def init(databasePath, tables):
    conn = connectToDatabase(databasePath)
    if conn is not None:
        initTables(conn, tables)
    conn.commit()


tables_sql = [
    """CREATE TABLE IF NOT EXISTS RegisteredUsers(
        username CHAR(30) PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'Customer'
    )""",

    """CREATE TABLE IF NOT EXISTS Items(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
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
          id INTEGER PRIMARY KEY AUTOINCREMENT ,
          title CHAR(30) NOT NULL,
          rank REAL,
          status TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ReviewsOnShops(
          reviewId INTEGER PRIMARY KEY AUTOINCREMENT ,
          writerId INTEGER REFERENCES RegisteredUsers(username),
          shopId INTEGER REFERENCES Shops(id),
          description TEXT,
          rank INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ReviewsOnItems(
          reviewId INTEGER PRIMARY KEY AUTOINCREMENT ,
          writerId INTEGER REFERENCES RegisteredUsers(username),
          itemId INTEGER REFERENCES Items(id),
          description TEXT,
          rank INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS PurchasedItems(
          purchaseId INTEGER PRIMARY KEY AUTOINCREMENT ,
          PurchasedItem INTEGER REFERENCES Items(id),
          purchasedData TEXT,
          userId CHAR(30) REFERENCES RegisteredUsers(username)
        )
    """,+
    """
        CREATE TABLE IF NOT EXISTS OwnersOfShops(
          userId CHAR(30) REFERENCES RegisteredUsers(username),
          shopId INTEGER REFERENCES Shops(id), 
          PRIMARY KEY(userId,shopId)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Messages(
          MessageId INTEGER PRIMARY KEY AUTOINCREMENT,
          MessageFrom CHAR(30),
          MessageTo CHAR(30),
          Content TEXT
        )
    """
]


def init_database(path):
    init(path, tables_sql)
    print('database initialized')


init_database('../db.sqlite3')
