from DatabaseLayer.getConn import commit_command


def add_owner(shop_id, receiver_user_id):
    sql = """
            INSERT INTO Owners (userId, shopId)
            VALUES ('{}','{}')
            """.format(receiver_user_id, shop_id)
    return commit_command(sql)


def modify_notifications(owner_id, should_notify):
    sql = """
            UPDATE Owners SET shouldNotify = '{}'
            WHERE userId like '{}'
            """.format(should_notify, owner_id)
    return commit_command(sql)
