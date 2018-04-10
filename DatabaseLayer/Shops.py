from DatabaseLayer.getConn import getConn


def searchShop(shop_name):
    c = getConn().cursor()
    c.execute("""
                SELECT *
                FROM Shops
                WHERE title = {}
              """.format(shop_name))
    return c.fetchall()


def create_shop(shop):
    c = getConn().cursor()
    c.execute("""
                INSERT INTO Shops (id, title, rank,
                 status)  
VALUES ({}, {}, {}, {});
              """.format(shop.id, shop.title,
                         shop.rank, shop.status))
    return c.fetchall()


def connect_shop_to_owner(shop, user_id):
    c = getConn().cursor()
    c.execute("""
                INSERT INTO OwnersOfShops (userId, shopId)  
VALUES ({}, {});
              """.format(user_id, shop.id))
    return c.fetchall()


def add_review_on_shop(writer_id, shop_id, description, rank):
    c = getConn().cursor()
    c.execute("""
                INSERT INTO ReviewsOnShops (writerId, shopId, description,
                 rank)  
VALUES ({}, {}, {}, {});
              """.format(writer_id, shop_id,
                         description, rank))
    return c.fetchall()
