from DatabaseLayer import Lotteries, RegisteredUsers
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


def add_lottery_and_items(item, ticket, item_price, final_date, username):
    if item is not None and ticket is not None and item_price is not None and final_date is not None and username is not None:
        item_id = ItemsLogic.add_item_to_shop_and_return_id(item, username)
        if item_id is not False:
            ticket_id = ItemsLogic.add_item_to_shop_and_return_id(ticket, username)
            if ticket_id is not False:
                lottery = Lottery(ticket_id, item_price, final_date, None, None, item_id)
                status = Lotteries.add_lottery(lottery)
                if status is not False:
                    return True
    return False
