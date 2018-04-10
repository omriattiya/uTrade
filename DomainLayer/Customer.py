from DatabaseLayer import Customers


def get_purchase_history(user_id):
    if user_id is not None:
        return Customers.get_purchase_history(user_id)

