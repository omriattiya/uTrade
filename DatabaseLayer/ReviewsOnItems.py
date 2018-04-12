from DatabaseLayer.getConn import commit_command, select_command


def add_review_on_item(writer_id, item_id, description, rank):
    sql_query = """
                INSERT INTO ReviewsOnItems (writerId, itemId, description, rank)  
                VALUES ('{}', '{}', '{}', '{}');
              """.format(writer_id, item_id,
                         description, rank)
    return commit_command(sql_query)


def get_all_reviews_on_item(item_id):
    sql_query = """
                SELECT *
                FROM ReviewsOnItems
                WHERE itemId = '{}'
              """.format(item_id)
    return select_command(sql_query)


def get_item_rank(item_id):
    sql_query = """
                SELECT AVG(rank)
                FROM ReviewsOnItems
                WHERE itemId = '{}'
                """.format(item_id)
    return select_command(sql_query)
