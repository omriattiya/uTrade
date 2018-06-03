import sqlite3
from sqlite3 import Error
is_test = False


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


def insert_defaults(conn, values):
    c = conn.cursor()
    try:
        for value in values:
            c.execute(value)
    except Error as e:
        print(e)


def init(database_path, tables, values):
    conn = connect_to_database(database_path)
    if conn is not None:
        init_tables(conn, tables)
        insert_defaults(conn, values)
    conn.commit()


tables_sql = [
    """CREATE TABLE IF NOT EXISTS RegisteredUsers(
        username CHAR(30) PRIMARY KEY,
        password TEXT NOT NULL,
        CONSTRAINT username_size CHECK(length(username) <= 30)
    )""",

    """CREATE TABLE IF NOT EXISTS Items(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE ,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        keyWords TEXT,
        price REAL NOT NULL,
        quantity INTEGER,
        kind TEXT,
        url TEXT,
        item_rating REAL,
        sum_of_rankings INTEGER,
        num_of_reviews INTEGER
    )""",
    """
        CREATE TABLE IF NOT EXISTS Shops(
          name CHAR(30) PRIMARY KEY NOT NULL,
          status TEXT,
          CONSTRAINT name_size CHECK(length(name) <= 30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ReviewsOnShops(
          reviewId INTEGER PRIMARY KEY AUTOINCREMENT ,
          writerId CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE SET NULL,
          shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE ,
          description TEXT,
          rank INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ReviewsOnItems(
          reviewId INTEGER PRIMARY KEY AUTOINCREMENT ,
          writerId CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE SET NULL ,
          itemId INTEGER REFERENCES Items(id) ON DELETE CASCADE ,
          description TEXT,
          rank INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Purchases(
          purchaseId INTEGER PRIMARY KEY AUTOINCREMENT ,
          purchaseDate DATE,
          username CHAR(30) REFERENCES RegisteredUsers(username),
          totalPrice REAL,
          CONSTRAINT username_size CHECK(length(username) <= 30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS PurchasedItems(
          purchaseId INTEGER REFERENCES Purchases(purchaseId) ,
          purchasedItem INTEGER REFERENCES Items(id) ON DELETE SET NULL,
          quantity INTEGER,
          price REAL,
          PRIMARY KEY(purchaseId,purchasedItem)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Owners(
          username CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE CASCADE ,
          shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE , 
          shouldNotify INTEGER DEFAULT 1,
          PRIMARY KEY(username,shop_name),
          CONSTRAINT username_size CHECK(length(username) <= 30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS Messages(
          MessageId INTEGER PRIMARY KEY AUTOINCREMENT,
          MessageFrom CHAR(30),
          MessageTo CHAR(30),
          Content TEXT,
          CONSTRAINT MessageFrom_size CHECK(length(MessageFrom) <= 30),
          CONSTRAINT MessageTo_size CHECK(length(MessageTo) <= 30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingCartItem(
          userName CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE CASCADE ,
          itemId INTEGER REFERENCES Items(id) ON DELETE CASCADE ,
          itemQuantity INTEGER,
          code CHAR(15) DEFAULT NULL,
          PRIMARY KEY(userName,itemId),
          CONSTRAINT userName_size CHECK(length(userName) <= 30),
          CONSTRAINT code_size CHECK(length(code) <= 15)
        )
    """,
    # TODO: whoever does this part needs to add more fields to the table below
    """
        CREATE TABLE IF NOT EXISTS PurchasePolicy(
          itemId INTEGER REFERENCES Items(id) ON DELETE CASCADE ,
          purchasePolicy TEXT,
          PRIMARY KEY(itemId)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS SystemManagers(
          username char(30),
          password TEXT NOT NULL,
          PRIMARY KEY(username),
          CONSTRAINT username_size CHECK(length(username) <= 30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS StoreManagers(
          username char(30) ,
          shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE ,
          addItemPermission INTEGER NOT NULL,
          removeItemPermission INTEGER NOT NULL,
          editItemPermission INTEGER NOT NULL,
          replyMessagePermission INTEGER NOT NULL,
          getAllMessagePermission INTEGER NOT NULL,
          getPurchaseHistoryPermission INTEGER NOT NULL,
          discountPermission INTEGER NOT NULL,
          FOREIGN KEY (username) REFERENCES RegisteredUsers(username) ON DELETE CASCADE ,
          PRIMARY KEY(username,shop_name),
          CONSTRAINT username_size CHECK(length(username) <= 30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS VisibleDiscounts(
          item_id INTEGER REFERENCES Items(id) ON DELETE CASCADE ,
          shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE ,
          percentage REAL,
          from_date DATE,
          end_date DATE,
          PRIMARY KEY(item_id, shop_name, from_date)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS InvisibleDiscounts(
          code CHAR(15),
          item_id INTEGER REFERENCES Items(id) ON DELETE CASCADE ,
          shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE ,
          percentage REAL,
          from_date DATE,
          end_date DATE,
          PRIMARY KEY(code),
          CONSTRAINT code_size CHECK(length(code) <= 15)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS GlobalDiscountInShop(
          shop_name CHAR(30) REFERENCES Shops(name) ON DELETE CASCADE,
          percentage REAL,
          from_date DATE,
          end_date DATE,
          code CHAR(15),
          PRIMARY KEY(shop_name, from_date),
          CONSTRAINT code_size CHECK(length(code) <= 15)
        )
    """,

    """
        CREATE TABLE IF NOT EXISTS Lotteries(
          lotto_id INTEGER REFERENCES Items(id),
          max_price INTEGER,
          final_date DATE,
          real_end_date DATE,
          winner CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE SET NULL ,
          prize_item_id INTEGER REFERENCES Items(id) ON DELETE SET NULL,
          PRIMARY KEY(lotto_id)
        )
    """,

    """
        CREATE TABLE IF NOT EXISTS CustomersInLotteries(
          lotto_id INTEGER REFERENCES Lotteries(lotto_id) ON DELETE CASCADE ,
          username CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE CASCADE ,
          price INTEGER,
          PRIMARY KEY(lotto_id,username)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS HistoryOfAppointing(
          historyId INTEGER PRIMARY KEY AUTOINCREMENT,
          appointingUser CHAR(30) REFERENCES RegisteredUsers(username),
          appointedUser CHAR(30) REFERENCES RegisteredUsers(username),
          position CHAR(10),
          shop_name CHAR(30) REFERENCES Shops(name),
          date CHAR(30),
          permissions CHAR(30)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS UserDetails(
          username CHAR(30) REFERENCES RegisteredUsers(username) ON DELETE CASCADE, 
          state CHAR(30) DEFAULT NULL,
          age INTEGER DEFAULT NULL,
          sex INTEGER DEFAULT NULL,
          PRIMARY KEY(username)
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingPolicyOnShop(
          policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
          shop_name CHAR(30) REFERENCES Shops(name),
          conditions TEXT,
          restriction TEXT,
          quantity INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingPolicyOnItems(
          policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
          item_name TEXT,
          conditions TEXT,
          restriction TEXT,
          quantity INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingPolicyOnCategory(
          policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
          category TEXT,
          conditions TEXT,
          restriction TEXT,
          quantity INTEGER
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS ShoppingPolicyOnIdentity(
          policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
          conditions TEXT,
          restriction TEXT,
          quantity INTEGER
        )
    """,
]
values_sql = [

    #       _        ___            _         _       _
    #      | |      / __)          | |_      (_)     (_)_
    #    _ | | ____| |__ ____ _   _| | |_     _ ____  _| |_
    #   / || |/ _  )  __) _  | | | | |  _)   | |  _ \| |  _)
    #  ( (_| ( (/ /| | ( ( | | |_| | | |__   | | | | | | |__
    #   \____|\____)_|  \_||_|\____|_|\___)  |_|_| |_|_|\___)
    #
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate_OmriOmri','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate_ShaharShahar','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate_TomerTomer','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate_YoniYoni','ADMINISTRATOR'); """,
    """ INSERT INTO SystemManagers (username, password) VALUES ('Ultimate_KutiKuti','ADMINISTRATOR'); """
]


def init_database(path):
    global is_test
    is_test = True
    init(path, tables_sql, values_sql)
    print('database initialized')


if __name__ == '__main__':
    init_database('../db.sqlite3')
