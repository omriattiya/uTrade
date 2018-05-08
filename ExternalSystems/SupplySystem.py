from datetime import datetime


def supply_a_purchase(username, address):
    return "A supply procedure for" + username + "was started on " + datetime.now().strftime("%c")\
           + "sent to address:" + address
