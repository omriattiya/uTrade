from sqlite3 import Error

from DatabaseLayer.getConn import get_conn, commit_command


def add_owner(shop_id, receiver_user_id):
    sql = """
            INSERT INTO Owners (userId, shopId)
            VALUES ({},{})
            """.format(receiver_user_id, shop_id)
    return commit_command(sql)


def add_manager(shop_id, target_user_id):
    sql = """
            INSERT INTO 
            """
    return commit_command(sql)
