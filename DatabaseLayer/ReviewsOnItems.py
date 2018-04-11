from DatabaseLayer.getConn import commit_command


def add_review_on_item(writer_id, item_id, description, rank):
    sql_query = """
                INSERT INTO ReviewsOnItems (writerId, itemId, description, rank)  
                VALUES ('{}', '{}', '{}', '{}');
              """.format(writer_id, item_id,
                         description, rank)
    return commit_command(sql_query)
