from datetime import datetime

from DatabaseLayer import Lotteries, RegisteredUsers, Purchases, PurchasedItems
from DomainLayer import ItemsLogic
from SharedClasses.Lottery import Lottery


def add_or_update_lottery_customer(purchased_item, username, price):
    if purchased_item is not None and username is not None and price is not None and price >= 0:
        lottery_customer = Lotteries.get_lottery_customer(purchased_item, username)
        user = RegisteredUsers.get_user(username)
        if user is not False:
            lottery = Lotteries.get_lottery(purchased_item)
            if lottery is not False:
                if lottery_customer is not False:
                    return Lotteries.update_lottery_item(purchased_item, username, price)
                else:
                    return Lotteries.add_lottery_item(purchased_item, username, price)
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
                lottery = Lottery(ticket_id, ticket_price, final_date, None, None, item_id)
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
                lottery = Lottery(ticket_id, ticket_price * ticket.quantity, final_date, None, None, item_id)
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
