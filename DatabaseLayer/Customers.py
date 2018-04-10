from DatabaseLayer.getConn import getConn


def get_purchase_history(user_id):
    c = getConn().cursor()
    c.execute("""
                SELECT *
                FROM PurchasedItems
                WHERE userId = {}
              """.format(user_id))
    return c.fetchall()