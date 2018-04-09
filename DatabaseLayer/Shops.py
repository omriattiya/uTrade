from DatabaseLayer.getConn import getConn

def searchShop(shop_name):
    c = getConn().cursor()
    c.execute("""
                SELECT *
                FROM Shops
                WHERE title = {}
              """.format(shop_name))
    return c.fetchall()