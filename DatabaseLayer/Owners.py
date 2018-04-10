from sqlite3 import Error

from DatabaseLayer.getConn import get_conn


def add_owner(shop_id, receiver_user_id):
    conn = get_conn()
    sql = """
            INSERT INTO Owners (userId, shopId)
            VALUES ({},{})
            """.format(receiver_user_id, shop_id)
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        return False
