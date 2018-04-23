from DatabaseLayer.getConn import select_command, commit_command


def add_lottery_item(purchased_item, user_id, price):
    sql_query = """
                INSERT INTO customersInLotteries(lotto_id,username,price)
                VALUES ('{}','{}','{}')
                """.format(purchased_item, user_id, price)
    return commit_command(sql_query)


def update_lottery_item(purchased_item, user_id, price):
    sql_query = """
                UPDATE customersInLotteries SET price = price + {}
                WHERE lotto_id = {} AND username ={})
                """.format(price, purchased_item, user_id)
    return commit_command(sql_query)


def get_lottery_customer(purchased_item, user_id):
    sql_query = """
                    SELECT *
                    FROM customersInLotteries
                    WHERE lotto_id = '{}' AND username = '{}'
                """.format(purchased_item, user_id)
    return fetch_purchased_item(select_command(sql_query))


def get_lottery(lottery_id):
    sql_query = """
                    SELECT *
                    FROM lotteries
                    WHERE lotto_id = '{}'
                """.format(lottery_id)
    return fetch_purchased_item(select_command(sql_query))