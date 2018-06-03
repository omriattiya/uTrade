from ExternalSystems.ExternalSystemInterfaces.PaymentInterface import PaymentInterface


class ProxyPaymentSystem(PaymentInterface):
    def pay(total_cost, username):
        return False
