from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.Shop import Shop


def parse_shops(shops):
    shops_list = []
    for shop in shops:
        shops_list.append(Shop(shop[0], shop[1]))
    return shops_list


def search_shop(shop_name):
    sql_query = """
                SELECT *
                FROM Shops
                WHERE name = '{}'
              """.format(shop_name)
    shop = select_command(sql_query)
    shop = parse_shops(shop)
    if len(shop) == 0:
        return False
    return shop[0]


def create_shop(shop):
    sql_query = """
                INSERT INTO Shops (name, status)  
                VALUES ('{}', '{}');
              """.format(shop.name, shop.status)
    return commit_command(sql_query)


def connect_shop_to_owner(username, shop_name):
    sql_query = """
                INSERT INTO Owners (username, shop_name)  
                VALUES ('{}', '{}')
              """.format(username, shop_name)
    return commit_command(sql_query)


def close_shop(shop_name):
    sql_query = """
            UPDATE Shops 
            SET status='Inactive'
            WHERE name='{}'
            """.format(shop_name)
    return commit_command(sql_query)


def re_open_shop(shop_name):
    sql_query = """
            UPDATE Shops 
            SET status='Active'
            WHERE name='{}' AND status != 'Permanently_closed'
            """.format(shop_name)
    return commit_command(sql_query)


def close_shop_permanently(shop_name):
    sql_query = """
            UPDATE Shops 
            SET status='Permanently_closed'
            WHERE name='{}'
            """.format(shop_name)
    return commit_command(sql_query)


def get_all_shops():
    sql_query = """
                    SELECT *
                    FROM Shops
                  """
    shops = select_command(sql_query)
    shops = parse_shops(shops)
    return shops
