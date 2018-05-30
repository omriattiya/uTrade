class ShoppingPolicyOnShop:
    def __init__(self, policy_id, shop_name, conditions, restrict, quantity):
        self.policy_id = policy_id
        self.item_name = shop_name
        self.conditions = conditions
        self.restrict = restrict
        self.quantity = quantity
