from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.Owner import Owner


def fetch_owners(results):
    array = []
    for item in results:
        array.append(Owner(item[0], item[1], item[2]))
    return array


def fetch_owner(result):
    if len(result) == 0:
        return False
    result = result[0]
    return Owner(result[0], result[1], result[2])


def add_owner(owner):
    sql = """
            INSERT INTO Owners (username, shop_name)
            VALUES ('{}','{}')
            """.format(owner.username, owner.shop_name)
    return commit_command(sql)


def modify_notifications(owner_username, should_notify, shop_name):
    sql = """
            UPDATE Owners SET shouldNotify = {}
            WHERE username = '{}' AND shop_name = '{}'
            """.format(should_notify, owner_username, shop_name)
    return commit_command(sql)


def get_owner(username, shop_name):
    sql_query = """
        SELECT * FROM Owners WHERE username = '{}' AND shop_name = '{}'
    """.format(username, shop_name)
    return fetch_owner(select_command(sql_query))


def is_owner(username):
    sql_query = """
           SELECT * FROM Owners WHERE username = '{}' 
       """.format(username)
    return len(select_command(sql_query)) >= 1


def remove_owner(username):
    sql = """
        SELECT shop_name FROM Owners  
        WHERE username = '{}'
    """.format(username)
    shops_array = select_command(sql)
    sql = """
               DELETE FROM Owners
               WHERE username = '{}'
             """.format(username)
    results = commit_command(sql)
    if results is not False:
        for i in range(0, len(shops_array)):
            sql = """
                SELECT * FROM Owners WHERE shop_name = '{}'
            """.format(shops_array[i][0])
            results = select_command(sql)
            if len(results) == 0:
                sql = """
                            UPDATE Shops 
                            SET status='Permanently_closed'
                            WHERE name='{}'
            """.format(shops_array[i][0])
                if not commit_command(sql):
                    return False
    else:
        return False
    return True


def get_shops_by_owner(username):
    sql_query = """
                    SELECT *
                    FROM Owners
                    WHERE username = '{}'
                  """.format(username)
    owned_shops = select_command(sql_query)
    owned_shops = fetch_owners(owned_shops)
    return owned_shops


def is_owner_on_shop(username, shop_name):
    sql_query = """
                        SELECT *
                        FROM Owners
                        WHERE username = '{}' AND shop_name = '{}'
                      """.format(username, shop_name)
    owned_shop = select_command(sql_query)
    return fetch_owner(owned_shop)


def get_owners_by_shop(shop_name):
    sql_query = """
                            SELECT *
                            FROM Owners
                            WHERE shop_name = '{}'
                          """.format(shop_name)
    owned_shop = select_command(sql_query)
    return fetch_owners(owned_shop)
