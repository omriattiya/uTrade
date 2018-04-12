from DatabaseLayer.getConn import commit_command, select_command


def add_owner(shop_name, username):
    sql = """
            INSERT INTO Owners (username, shop_name)
            VALUES ('{}','{}')
            """.format(username, shop_name)
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
    results = select_command(sql_query)
    if len(results) == 0:
        return False
    return results
