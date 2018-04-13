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

