from DatabaseLayer.getConn import commit_command


def add_review_on_shop(writer_id, shop_name, description, rank):
    sql_query = """
                INSERT INTO ReviewsOnShops (writerId, shop_name, description, rank)
                VALUES ('{}', '{}', '{}', '{}')
              """.format(writer_id, shop_name, description, rank)
    return commit_command(sql_query)
