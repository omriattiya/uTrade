from datetime import datetime

from ExternalSystems.ExternalSystemInterfaces.PaymentInterface import PaymentInterface


class PaymentSystem(PaymentInterface):
    def pay(self,total_cost, username):
        purchase_time = datetime.now()
        if total_cost > 0 and username is not None and username != "":
            if username[0:5] == 'guest':
                return "On " + purchase_time.strftime("%c") + " a payment of " + str(
                    total_cost) + " was made by guest and APPROVED by the Payment System."
            else:
                return "On " + purchase_time.strftime("%c") + " a payment of " + str(
                    total_cost) + " was made by the user:" + \
                       username + " and APPROVED by the Payment System."
        else:
            return False
