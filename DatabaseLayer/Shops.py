from DatabaseLayer.getConn import get_conn, commit_command
from sqlite3 import Error
from SharedClasses.Shop import Shop


def get_shop(shop_name):
    sql = """
                SELECT *
                FROM Shops
                WHERE title = '{}'
            """.format(shop_name)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(sql)
        shop = c.fetchone()
        if shop is None:
            return False
        shop = Shop( shop[1], shop[2], shop[3])
        conn.close()
        return shop
    except Error as e:
        return False


def searchShop(shop_name):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Shops
                WHERE title = '{}'
              """.format(shop_name))
    return c.fetchall()


def create_shop(shop):
    sql = """
                INSERT INTO Shops (title, status)  
    VALUES ('{}', '{}');
              """.format(shop.title, shop.status)
    return commit_command(sql)


def connect_shop_to_owner(shop_name, username):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO Owners (username, shop_name)  
VALUES ('{}', '{}');
              """.format(username, shop_name))
    return c.fetchall()


def close_shop(shop_name):
    sql = """
            UPDATE Shops 
            SET status='INACTIVE'
            WHERE title='{}'
            """.format(shop_name)
    return commit_command(sql)


def re_open_shop(shop_name):
    sql = """
            UPDATE Shops 
            SET status='ACTIVE'
            WHERE title='{}'
            """.format(shop_name)
    return commit_command(sql)


def close_shop_permanently(shop_name):
    sql = """
            UPDATE Shops 
            SET status='CLOSED'
            WHERE title='{}'
            """.format(shop_name)
    return commit_command(sql)
