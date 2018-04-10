from DatabaseLayer.getConn import get_conn


def searchItemsByName(item_name):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Items
                WHERE name = {}
              """.format(item_name))
    return c.fetchall()


def add_item_to_shop(item):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO Items (id, shopid, name,
                 category, keyWords,
                  rank, price, quantity)  
VALUES ({}, {}, {}, {}, {}, {}, {}, {});
              """.format(item.id, item.shop_id,
                         item.name, item.category,
                         item.keyWords, item.rank,
                         item.price, item.quantity))
    return c.fetchall()


def remove_item_from_shop(item_id):
    c = get_conn().cursor()
    c.execute("""
                DELETE FROM Items
                WHERE id = {}
              """.format(item_id))
    return c.fetchall()


def searchItemInShop(item_name, shop_name):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Items,Shops
                WHERE Items.name = {}  AND Shops.name = {} AND Items.shopId = Shops.id
              """.format(item_name, shop_name))
    return c.fetchall()


def searchItemsByCategory(item_category):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Items
                WHERE name = {}
              """.format(item_category))
    return c.fetchall()


def searchItemsByKeywords(item_keyword):
    c = get_conn().cursor()
    c.execute("""
                SELECT *
                FROM Items
                WHERE name = {}
              """.format(item_keyword))
    return c.fetchall()


def add_review_on_item(writer_id, item_id, description, rank):
    c = get_conn().cursor()
    c.execute("""
                INSERT INTO ReviewsOnItems (writerId, itemId, description,
                 rank)  
VALUES ({}, {}, {}, {});
              """.format(writer_id, item_id,
                         description, rank))
    return c.fetchall()
