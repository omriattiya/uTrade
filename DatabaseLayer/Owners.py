from DatabaseLayer.getConn import commit_command, get_conn


def add_owner(shop_title, receiver_user_id):
    sql = """
            INSERT INTO Owners (userId, shop_title)
            VALUES ('{}','{}')
            """.format(receiver_user_id, shop_title)
    return commit_command(sql)


def modify_notifications(owner_id, should_notify):
    sql = """
            UPDATE Owners SET shouldNotify = '{}'
            WHERE userId like '{}'
            """.format(should_notify, owner_id)
    return commit_command(sql)


def get_owner(username, shop_id):
    conn = get_conn()
    c = conn.cursor()
    sql = """
        SELECT * FROM Owners WHERE userId LIKE '{}' and shopId = {}
    """.format(username, shop_id)
    c.execute(sql)
    results = c.fetchall()
    conn.close()
    if len(results) == 1:
        return results
    return False
