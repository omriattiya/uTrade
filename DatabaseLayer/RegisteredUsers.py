from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.RegisteredUser import RegisteredUser


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
    results = select_command(sql_query)
    if len(results) == 0:
        return False
    return RegisteredUser(results[0][0], results[0][1])


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
                SELECT *
                FROM PurchasedItems
                WHERE username = '{}'
              """.format(username)
    return select_command(sql_query)
