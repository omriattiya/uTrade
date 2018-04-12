import sqlite3
from sqlite3 import Error


def connect_to_database(database_path):
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except Error as e:
        print(e)
        pass


def init_tables(conn, tables):
    c = conn.cursor()
    try:
        for table in tables:
            c.execute(table)
    except Error as e:
        print(e)


def init(database_path, tables):
    conn = connect_to_database(database_path)
    if conn is not None:
        init_tables(conn, tables)
    conn.commit()


tables_sql = [
    """CREATE TABLE IF NOT EXISTS RegisteredUsers(
        username CHAR(30) PRIMARY KEY,
        password TEXT NOT NULL
    )""",

    """CREATE TABLE IF NOT EXISTS Items(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        shop_name INTEGER REFERENCES Shops(name),
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        keyWords TEXT,
        price REAL NOT NULL,
        quantity INTEGER
    )""",
    """
        CREATE TABLE IF NOT EXISTS Shops(
          name CHAR(30) PRIMARY KEY NOT NULL,
          status TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ReviewsOnShops(
          reviewId INTEGER PRIMARY KEY AUTOINCREMENT ,
          writerId INTEGER REFERENCES RegisteredUsers(username),
          shop_name INTEGER REFERENCES Shops(name),
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
          purchaseDate INTEGER,
          quantity INTEGER,
          price REAL,
          username CHAR(30) REFERENCES RegisteredUsers(username)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Owners(
          username CHAR(30) REFERENCES RegisteredUsers(username),
          shop_name INTEGER REFERENCES Shops(name), 
          shouldNotify INTEGER DEFAULT 1,
          PRIMARY KEY(username,shop_name)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Messages(
          MessageId INTEGER PRIMARY KEY AUTOINCREMENT,
          MessageFrom CHAR(30),
          MessageTo CHAR(30),
          Content TEXT
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingCart(
          userName CHAR(30) REFERENCES RegisteredUsers(username),
          itemId INTEGER REFERENCES Items(id),
          itemQuantity INTEGER,
          code CHAR(15),
          PRIMARY KEY(userName,itemId)
        )
    """,
    # TODO: whoever does this part needs to add more fields to the table below
    """
        CREATE TABLE IF NOT EXISTS PurchasePolicy(
          itemId INTEGER REFERENCES Items(id),
          purchasePolicy TEXT,
          PRIMARY KEY(itemId)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS SystemManagers(
          username char(30),
          password TEXT NOT NULL,
          PRIMARY KEY(username)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS StoreManagers(
          username char(30) ,
          shop_name INTEGER REFERENCES Shops(name),
          addItemPermission INTEGER NOT NULL,
          removeItemPermission INTEGER NOT NULL,
          editItemPermission INTEGER NOT NULL,
          replyMessagePermission INTEGER NOT NULL,
          getAllMessagePermission INTEGER NOT NULL,
          getPurchaseHistoryPermission INTEGER NOT NULL,
          FOREIGN KEY (username) REFERENCES RegisteredUsers(username),
          PRIMARY KEY(username,shop_name)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS VisibleDiscounts(
          item_id INTEGER REFERENCES Items(id) ,
          shop_name INTEGER REFERENCES Shops(name),
          percentage REAL,
          from_date DATE,
          end_date DATE,
          PRIMARY KEY(item_id, shop_name, from_date)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS InvisibleDiscounts(
          item_id INTEGER REFERENCES Items(id) ,
          shop_name INTEGER REFERENCES Shops(name),
          percentage REAL,
          from_date DATE,
          end_date DATE,
          code CHAR(15),
          PRIMARY KEY(item_id, shop_name, from_date)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS GlobalDiscountInShop(
          shop_name INTEGER REFERENCES Shops(name),
          percentage REAL,
          from_date DATE,
          end_date DATE,
          code CHAR(15),
          PRIMARY KEY(shop_name, from_date)
        )
    """,
    #       _        ___            _         _       _
    #      | |      / __)          | |_      (_)     (_)_
    #    _ | | ____| |__ ____ _   _| | |_     _ ____  _| |_
    #   / || |/ _  )  __) _  | | | | |  _)   | |  _ \| |  _)
    #  ( (_| ( (/ /| | ( ( | | |_| | | |__   | | | | | | |__
    #   \____|\____)_|  \_||_|\____|_|\___)  |_|_| |_|_|\___)
    #
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate Omri','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate Shahar','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate Tomer','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate Yoni','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate Kuti','ADMINISTRATOR'); """
]


def init_database(path):
    init(path, tables_sql)
    print('database initialized')


init_database('../db.sqlite3')
