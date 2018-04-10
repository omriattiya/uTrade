from DatabaseLayer.getConn import get_conn, commit_command


def searchShop(shop_name):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Shops
                WHERE title = '{}'
              """.format(shop_name))
    return c.fetchall()


def create_shop(shop):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO Shops (id, title, rank,
                 status)  
VALUES ('{}', '{}', '{}', '{}');
              """.format(shop.id, shop.title,
                         shop.rank, shop.status))
    return c.fetchall()


def connect_shop_to_owner(shop, user_id):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO Owners (userId, shopId)  
VALUES ('{}', '{}');
              """.format(user_id, shop.id))
    return c.fetchall()


def add_review_on_shop(writer_id, shop_id, description, rank):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO ReviewsOnShops (writerId, shopId, description,
                 rank)  
VALUES ('{}', '{}', '{}', '{}');
              """.format(writer_id, shop_id,
                         description, rank))
    return c.fetchall()


def close_shop(shop_id):
    sql = """
            UPDATE Shops 
            SET status='INACTIVE'
            WHERE id='{}'
            """.format(shop_id)
    return commit_command(sql)


def re_open_shop(shop_id):
    sql = """
            UPDATE Shops 
            SET status='ACTIVE'
            WHERE id='{}'
            """.format(shop_id)
    return commit_command(sql)
