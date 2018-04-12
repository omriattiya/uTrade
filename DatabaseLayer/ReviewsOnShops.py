from DatabaseLayer.getConn import commit_command, select_command


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
    return select_command(sql_query)


def get_shop_rank(shop_name):
    sql_query = """
                SELECT AVG(rank)
                FROM ReviewsOnShops
                WHERE shop_name = '{}'
                """.format(shop_name)
    return select_command(sql_query)
