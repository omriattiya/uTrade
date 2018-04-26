
def charge_from_user(total_cost, balance):
    if total_cost < 0 or balance <= 0:
        return False
    if total_cost < balance:
        return False
    else:
        return balance - total_cost
