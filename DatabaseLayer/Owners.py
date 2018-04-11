from DatabaseLayer.getConn import commit_command, select_command


def add_owner(shop_name, username):
    sql = """
            INSERT INTO Owners (username, shop_name)
            VALUES ('{}','{}')
            """.format(username, shop_name)
    return commit_command(sql)


def modify_notifications(owner_id, should_notify):
    sql = """
            UPDATE Owners SET shouldNotify = '{}'
            WHERE username like '{}'
            """.format(should_notify, owner_id)
    return commit_command(sql)


def get_owner(username, shop_name):
    sql_query = """
        SELECT * FROM Owners WHERE username LIKE '{}' and shop_name = '{}'
    """.format(username, shop_name)
    results = select_command(sql_query)
    if len(results) == 1:
        return results
    return False
