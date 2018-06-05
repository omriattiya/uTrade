from DatabaseLayer.getConn import select_command, commit_command
from SharedClasses.Lottery import Lottery
from SharedClasses.LotteryCustomer import LotteryCustomer


def fetch_lottery(result):
    if len(result) == 0:
        return False
    result = result[0]
    return Lottery(result[0], result[1], result[2], result[3])


def fetch_lotteries(lotteries):
    lotteries_arr = []
    for item in lotteries:
        lotteries_arr.append(Lottery(item[0], item[1], item[2], item[3]))
    return lotteries_arr


def fetch_lottery_customer(result):
    if len(result) == 0:
        return False
    result = result[0]
    return LotteryCustomer(result[0], result[1], result[2], result[3])


def fetch_lottery_customers(result):
    arr = []
    for cus in result:
        arr.append(LotteryCustomer(cus[0], cus[1], cus[2], cus[3]))
    return arr


def fetch_integer(result):
    if len(result) == 0:
        return False
    return result[0]


def add_lottery(lottery):
    sql_query = """
                INSERT INTO Lotteries(lotto_id,final_date,prize_item_id)
                VALUES ('{}','{}','{}')
                """.format(lottery.lotto_id, lottery.final_date, lottery.prize_item_id)
    return commit_command(sql_query)


def add_lottery_item(purchased_item, user_id, price, number_of_tickets):
    sql_query = """
                INSERT INTO CustomersInLotteries(lotto_id,username,price,number_of_tickets)
                VALUES ('{}','{}','{}','{}')
                """.format(purchased_item, user_id, price, number_of_tickets)
    return commit_command(sql_query)


def update_lottery_item(purchased_item, user_id, price, number_of_tickets):
    sql_query = """
                UPDATE CustomersInLotteries SET price = price + {} AND number_of_tickets = number_of_tickets + {}
                WHERE lotto_id = {} AND username ={})
                """.format(price, number_of_tickets, purchased_item, user_id)
    return commit_command(sql_query)


def update_lottery_real_date(purchased_item, end_date):
    sql_query = """
                UPDATE Lotteries SET real_end_date = '{}'
                WHERE lotto_id = {}
                """.format(end_date, purchased_item)
    return commit_command(sql_query)


def get_lottery_customer(purchased_item, user_id):
    sql_query = """
                    SELECT *
                    FROM CustomersInLotteries
                    WHERE lotto_id = '{}' AND username = '{}'
                """.format(purchased_item, user_id)
    return fetch_lottery_customer(select_command(sql_query))


def get_lottery_customers(purchased_item):
    sql_query = """
                    SELECT *
                    FROM CustomersInLotteries
                    WHERE lotto_id = '{}'
                """.format(purchased_item)
    return fetch_lottery_customers(select_command(sql_query))


def get_lottery(lottery_id):
    sql_query = """
                    SELECT *
                    FROM Lotteries
                    WHERE lotto_id = '{}'
                """.format(lottery_id)
    return fetch_lottery(select_command(sql_query))


def get_lotteries():
    sql_query = """
                    SELECT *
                    FROM Lotteries
                """
    return fetch_lotteries(select_command(sql_query))


def get_lottery_sum(lottery_id):
    sql_query = """
                    SELECT SUM(price)
                    FROM CustomersInLotteries
                    WHERE lotto_id = '{}'
                """.format(lottery_id)
    number = fetch_integer(select_command(sql_query))
    if number[0] is None:
        return 0
    return number[0]


def get_prize(lottery_id):
    sql_query = """ SELECT prize_item_id
                        FROM Lotteries
                        WHERE lotto_id = '{}'
                    """.format(lottery_id)
    number = fetch_integer(select_command(sql_query))
    if number[0] is None:
        return 0
    return number[0]
