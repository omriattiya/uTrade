from DatabaseLayer.getConn import get_conn


def get_purchase_history(user_id):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM PurchasedItems
                WHERE userId = '{}'
              """.format(user_id))
    return c.fetchall()