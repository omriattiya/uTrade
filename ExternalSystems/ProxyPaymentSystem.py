from ExternalSystems.ExternalSystemInterfaces.PaymentInterface import PaymentInterface


class ProxyPaymentSystem(PaymentInterface):
    def pay(self,total_cost, username):
        return False
