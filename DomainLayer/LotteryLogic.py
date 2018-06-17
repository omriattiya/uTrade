import random
import threading
from datetime import datetime

from DatabaseLayer import Lotteries, RegisteredUsers, Purchases, PurchasedItems
from DomainLayer import ItemsLogic
from SharedClasses.Lottery import Lottery
from ServiceLayer.services.LiveAlerts import LoterryAlerts


def add_or_update_lottery_customer(purchased_item, username, price, number_of_tickets):
    if purchased_item is not None and username is not None and price is not None and price >= 0:
        lottery_customer = Lotteries.get_lottery_customer(purchased_item, username)
        user = RegisteredUsers.get_user(username)
        if user is not False:
            lottery = Lotteries.get_lottery(purchased_item)
            if lottery is not False:
                if lottery_customer is not False:
                    return Lotteries.update_lottery_item(purchased_item, username, price, number_of_tickets)
                else:
                    return Lotteries.add_lottery_item(purchased_item, username, price, number_of_tickets)
            else:
                print("No such lottery")
        else:
            print("No such user")
    return False


def add_lottery_and_items(prize, ticket, ticket_price, final_date, username):
    if prize is not None and ticket is not None and ticket_price is not None and final_date is not None and username is not None:
        item_id = ItemsLogic.add_item_to_shop_and_return_id(prize, username)
        if item_id is not False:
            ticket_id = ItemsLogic.add_item_to_shop_and_return_id(ticket, username)
            if ticket_id is not False:
                lottery = Lottery(ticket_id, final_date, None, item_id)
                status = Lotteries.add_lottery(lottery)
                if status is not False:
                    return True
    return False


def add_lottery_and_items_and_return_id(prize, ticket, ticket_price, final_date, username):
    if prize is not None and ticket is not None and ticket_price is not None and final_date is not None and username is not None:
        item_id = ItemsLogic.add_item_to_shop_and_return_id(prize, username)
        if item_id is not False:
            ticket_id = ItemsLogic.add_item_to_shop_and_return_id(ticket, username)
            if ticket_id is not False:
                lottery = Lottery(ticket_id, final_date, None, item_id)
                status = Lotteries.add_lottery(lottery)
                if status is not False:
                    return ticket_id
    return False


def win_lottery(username, prize_id, price):
    purchase_id = Purchases.add_purchase_and_return_id(datetime.now(), username, 0)
    status = PurchasedItems.add_purchased_item(purchase_id, prize_id, 1,
                                               price)
    return status


def get_lottery_customers(purchase_id):
    return Lotteries.get_lottery_customers(purchase_id)


def get_prize_id(lottery_id):
    return Lotteries.get_prize(lottery_id)


def start_lottery(status, sale_date, sale_hour, sale_minutes):
    lottery_date = datetime.strptime(sale_date + ' ' + sale_hour + ':' + sale_minutes, '%Y-%m-%d %H:%M')
    today = datetime.now()
    subtraction = lottery_date - today
    threading.Timer(subtraction.total_seconds(), lottery_timer, [status]).start()


def lottery_timer(lottery_id):
    lottery = Lotteries.get_lottery(lottery_id)
    if lottery.real_end_date is not None:
        return
    ticket = ItemsLogic.get_item(lottery_id)
    lottery_customers = get_lottery_customers(lottery_id)
    if ticket.quantity > 0:
        Lotteries.update_lottery_real_date(lottery_id, datetime.now().strftime("%Y-%m-%d %H:%M"))
        customer_names = []
        for customer in lottery_customers:
            # TODO add live alert to customers
            customer_names.append(customer.username)
        LoterryAlerts.notify_lottery_alerts(customer_names,
                                             'Lottery for item  <a href="http://localhost:8000/app/item/?item_id='
                                             + str(lottery_id) + '"># <strong>' + str(
                                                 lottery_id) + '</strong></a> has been canceled.')


def activate_lottery(lottery_id):
    lottery = Lotteries.get_lottery(lottery_id)
    if lottery.real_end_date is not None:
        return
    lottery_customers = get_lottery_customers(lottery_id)
    prize_id = get_prize_id(lottery_id)
    numbers = []
    i = 0
    for cus in lottery_customers:
        numbers.append(i + cus.number_of_tickets - 1)
        i += cus.number_of_tickets
    winner = random.randint(0, i - 1)
    index = 0
    while index < len(numbers):
        if numbers[index] >= winner:
            # TODO add live alert to winner customer
            LoterryAlerts.notify_lottery_alerts([lottery_customers[index].username],
                                                'You have won item  <a href="http://localhost:8000/app/item/?item_id='
                                                + str(lottery_id) + '"># <strong>' + str(
                                                    lottery_id) + '</strong></a> in a lottery.')
            win_lottery(lottery_customers[index].username, prize_id, lottery_customers[index].price)
            break
        index = index + 1
    Lotteries.update_lottery_real_date(lottery_id, Lotteries.get_lottery(lottery_id).final_date)


def search_for_unfinished_lotteries():
    lotteries = Lotteries.get_lotteries()
    for lottery in lotteries:
        if lottery.real_end_date is None:
            lottery_date = datetime.strptime(lottery.final_date, '%Y-%m-%d %H:%M')
            if datetime.now() > lottery_date:
                Lotteries.update_lottery_real_date(lottery.lotto_id, lottery_date)
            else:
                start_lottery(lottery.lotto_id, lottery_date.strftime("%Y-%m-%d"), lottery_date.hour, lottery_date.minute)

