from datetime import datetime


def pay(total_cost, username):
    purchase_time = datetime.now()
    return "On " + purchase_time.strftime("%c") + " a payment of " + total_cost + " was made by the user:" + username
