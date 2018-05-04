from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.ItemReview import ItemReview


def fetch_reviews(results):
    array = []
    for item in results:
        array.append(ItemReview(item[1], item[2], item[3], item[4]))
    return array


def fetch_review(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ItemReview(result[0], result[1], result[2], result[3])


def add_review_on_item(review):
    sql_query = """
                INSERT INTO ReviewsOnItems (writerId, itemId, description, rank)  
                VALUES ('{}', '{}', '{}', '{}');
              """.format(review.writerId, review.itemId,
                         review.description, review.rank)
    return commit_command(sql_query)


def get_all_reviews_on_item(item_id):
    sql_query = """
                SELECT *
                FROM ReviewsOnItems
                WHERE itemId = '{}'
              """.format(item_id)
    return fetch_reviews(select_command(sql_query))


def get_item_rank(item_id):
    sql_query = """
                SELECT AVG(rank)
                FROM ReviewsOnItems
                WHERE itemId = '{}'
                """.format(item_id)
    return select_command(sql_query)[0][0]
