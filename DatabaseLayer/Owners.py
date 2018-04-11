from DatabaseLayer.getConn import commit_command, get_conn


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
    conn = get_conn()
    c = conn.cursor()
    sql = """
        SELECT * FROM Owners WHERE username LIKE '{}' and shop_name = {}
    """.format(username, shop_name)
    c.execute(sql)
    results = c.fetchall()
    conn.close()
    if len(results) == 1:
        return results
    return False
