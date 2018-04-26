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


def modify_notifications(owner_username, should_notify):
    sql = """
            UPDATE Owners SET shouldNotify = {}
            WHERE username = '{}'
            """.format(should_notify, owner_username)
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
    for i in range(0, len(shops_array)):
        sql = """
            SELECT * FROM Owners WHERE shop_name = '{}'
        """.format(shops_array[i])
        results = select_command(sql)
        if len(results) == 1:
            sql = """
                        DELETE FROM Shops
                        WHERE name = '{}'
                      """.format(shops_array[i])
            if not commit_command(sql):
                return False
    return True
