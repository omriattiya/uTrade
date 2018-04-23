from DatabaseLayer.getConn import select_command, commit_command
from SharedClasses.Lottery import Lottery
from SharedClasses.LotteryCustomer import LotteryCustomer

def fetch_lottery(result):
    if len(result) == 0:
        return False
    result = result[0]
    return Lottery(result[0], result[1], result[2], result[3], result[4], result[5])


def fetch_lottery_customer(result):
    if len(result) == 0:
        return False
    result = result[0]
    return LotteryCustomer(result[0], result[1], result[2])


def fetch_integer(result):
    if len(result) == 0:
        return False
    return result[0]

def add_lottery_item(purchased_item, user_id, price):
    sql_query = """
                INSERT INTO CustomersInLotteries(lotto_id,username,price)
                VALUES ('{}','{}','{}')
                """.format(purchased_item, user_id, price)
    return commit_command(sql_query)


def update_lottery_item(purchased_item, user_id, price):
    sql_query = """
                UPDATE CustomersInLotteries SET price = price + {}
                WHERE lotto_id = {} AND username ={})
                """.format(price, purchased_item, user_id)
    return commit_command(sql_query)


def get_lottery_customer(purchased_item, user_id):
    sql_query = """
                    SELECT *
                    FROM CustomersInLotteries
                    WHERE lotto_id = '{}' AND username = '{}'
                """.format(purchased_item, user_id)
    return fetch_lottery_customer(select_command(sql_query))


def get_lottery(lottery_id):
    sql_query = """
                    SELECT *
                    FROM Lotteries
                    WHERE lotto_id = '{}'
                """.format(lottery_id)
    return fetch_lottery(select_command(sql_query))


def get_lottery_sum(lottery_id):
    sql_query = """
                    SELECT SUM(price)
                    FROM CustomersInLotteries
                    WHERE lotto_id = '{}'
                """.format(lottery_id)
    return fetch_integer(select_command(sql_query))
