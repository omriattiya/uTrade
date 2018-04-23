from DatabaseLayer import Lotteries, RegisteredUsers


def add_or_update_lottery_customer(purchased_item, username, price):
    if purchased_item is not None and username is not None and price is not None:
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


def add_lottery(lottery):
    if lottery is not None:
        return Lotteries.add_lottery(lottery)
