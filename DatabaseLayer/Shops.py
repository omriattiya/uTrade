from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.Shop import Shop


def search_shop(shop_name):
    sql_query = """
                SELECT *
                FROM Shops
                WHERE name = '{}'
              """.format(shop_name)
    shop = select_command(sql_query)
    if len(shop) == 0:
        return False
    shop = shop[0]
    return Shop(shop[0], shop[1])


def create_shop(shop):
    sql_query = """
                INSERT INTO Shops (name, status)  
                VALUES ('{}', '{}');
              """.format(shop.name, shop.status)
    return commit_command(sql_query)


def connect_shop_to_owner(shop, shop_name):
    sql_query = """
                INSERT INTO Owners (username, shop_name)  
                VALUES ('{}', '{}')
              """.format(shop_name, shop.name)
    return commit_command(sql_query)


def close_shop(shop_name):
    sql_query = """
            UPDATE Shops 
            SET status='INACTIVE'
            WHERE name='{}'
            """.format(shop_name)
    return commit_command(sql_query)


def re_open_shop(shop_name):
    sql_query = """
            UPDATE Shops 
            SET status='ACTIVE'
            WHERE name='{}'
            """.format(shop_name)
    return commit_command(sql_query)


def close_shop_permanently(shop_name):
    sql_query = """
            UPDATE Shops 
            SET status='CLOSED'
            WHERE name='{}'
            """.format(shop_name)
    return commit_command(sql_query)
