from DatabaseLayer.getConn import commit_command


def add_owner(shop_id, receiver_user_id):
    sql = """
            INSERT INTO Owners (userId, shopId)
            VALUES ('{}','{}')
            """.format(receiver_user_id, shop_id)
    return commit_command(sql)


