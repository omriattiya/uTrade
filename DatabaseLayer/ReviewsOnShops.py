from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.ShopReview import ShopReview


def fetch_reviews(results):
    array = []
    for item in results:
        array.append(ShopReview(item[0], item[1], item[2], item[3]))
    return array


def fetch_review(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ShopReview(result[0], result[1], result[2], result[3])


def add_review_on_shop(writer_id, shop_name, description, rank):
    sql_query = """
                INSERT INTO ReviewsOnShops (writerId, shop_name, description, rank)
                VALUES ('{}', '{}', '{}', '{}')
              """.format(writer_id, shop_name, description, rank)
    return commit_command(sql_query)


def get_all_reviews_on_shop(shop_name):
    sql_query = """
                SELECT *
                FROM ReviewsOnShops
                WHERE shop_name = '{}'
              """.format(shop_name)
    return fetch_reviews(select_command(sql_query))


def get_shop_rank(shop_name):
    sql_query = """
                SELECT AVG(rank)
                FROM ReviewsOnShops
                WHERE shop_name = '{}'
                """.format(shop_name)
    return select_command(sql_query)[0][0]
