from DatabaseLayer.getConn import commit_command, select_command


def add_owner(shop_name, receiver_username):
    sql = """
            INSERT INTO Owners (username, shop_name)
            VALUES ('{}','{}')
            """.format(receiver_username, shop_name)
    return commit_command(sql)


def modify_notifications(owner_id, should_notify):
    sql = """
            UPDATE Owners SET shouldNotify = '{}'
            WHERE username like '{}'
            """.format(should_notify, owner_id)
    return commit_command(sql)


def get_owner(username, shop_name):
    sql_query = """
        SELECT * FROM Owners WHERE username LIKE '{}' AND shop_name = '{}'
    """.format(username, shop_name)
    results = select_command(sql_query)
    return results

