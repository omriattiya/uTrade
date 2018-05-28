from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.RegisteredUser import RegisteredUser
from DatabaseLayer.PurchasedItems import fetch_purchased_items


def fetch_users(results):
    array = []
    for item in results:
        array.append(RegisteredUser(item[0], item[1]))
    return array


def fetch_user(result):
    if len(result) == 0:
        return False
    result = result[0]
    return RegisteredUser(result[0], result[1])


def add_user(user):
    sql_query = """
            INSERT INTO RegisteredUsers(username,password)
            VALUES ('{}','{}')
            """.format(user.username, user.password)
    return commit_command(sql_query)


def edit_user_password(user):
    sql_query = """
            UPDATE RegisteredUsers
            SET password = '{}'
            WHERE username = '{}'
            """.format(user.password, user.username)
    return commit_command(sql_query)


def get_user(username):
    sql_query = """
            SELECT *
            FROM RegisteredUsers
            WHERE username = '{}'
            """.format(username)
    return fetch_user(select_command(sql_query))


def login(user):
    sql_query = """
            SELECT *
            FROM RegisteredUsers
            WHERE username = '{}' AND password = '{}'
            """.format(user.username, user.password)
    return len(select_command(sql_query)) == 1


def remove_user(registered_user):
    sql = """
                DELETE FROM RegisteredUsers
                WHERE username = '{}'
              """.format(registered_user)
    return commit_command(sql)


def get_purchase_history(username):
    sql_query = """
                SELECT PurchasedItems.*
                FROM PurchasedItems,Purchases
                WHERE Purchases.purchaseId = PurchasedItems.purchaseId AND Purchases.username = '{}'
              """.format(username)
    return fetch_purchased_items(select_command(sql_query))


def get_all_users():
    sql_query = """
                SELECT *
                FROM RegisteredUsers
              """
    return fetch_users(select_command(sql_query))


def is_user_exists(username):
    sql_query = """
                SELECT *
                FROM RegisteredUsers
                WHERE username = '{}'
                """.format(username)
    return len(select_command(sql_query)) == 1
