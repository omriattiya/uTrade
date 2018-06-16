from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.ShopReview import ShopReview


def fetch_reviews(results):
    array = []
    for item in results:
        array.append(ShopReview(item[1], item[3], item[4], item[2]))
    return array


def fetch_review(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ShopReview(result[1], result[3], result[4], result[2])


def add_review_on_shop(shop_review):
    sql_query = """
                INSERT INTO ReviewsOnShops (writerId, shop_name, description, rank)
                VALUES ('{}', '{}', '{}', '{}')
              """.format(shop_review.writerId, shop_review.shop_name, shop_review.description, shop_review.rank)
    return commit_command(sql_query)


def get_all_reviews_on_shop(shop_name):
    sql_query = """
                SELECT *
                FROM ReviewsOnShops
                WHERE shop_name = '{}'
              """.format(shop_name)
    return fetch_reviews(select_command(sql_query))


def get_review_on_shop_by_writer(shop_name, writer_id):
    sql_query = """
                SELECT *
                FROM ReviewsOnShops
                WHERE shop_name = '{}' AND writerId = '{}'
              """.format(shop_name,writer_id)
    return fetch_review(select_command(sql_query))


def get_shop_rank(shop_name):
    sql_query = """
                SELECT AVG(rank)
                FROM ReviewsOnShops
                WHERE shop_name = '{}'
                """.format(shop_name)
    return select_command(sql_query)[0][0]
