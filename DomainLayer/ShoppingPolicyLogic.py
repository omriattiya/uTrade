from DatabaseLayer import ShoppingPolicies

#    ____________________________________   GET ALL     ___________________________________________________


def get_all_shopping_policy_on_shop():
    return ShoppingPolicies.get_all_shopping_policy_on_shop()


def get_all_shopping_policy_on_items():
    return ShoppingPolicies.get_all_shopping_policy_on_items()


def get_all_shopping_policy_on_category():
    return ShoppingPolicies.get_all_shopping_policy_on_category()


def get_all_shopping_policy_on_identity():
    return ShoppingPolicies.get_all_shopping_policy_on_identity()


#    ____________________________________   INSERT     ___________________________________________________


def add_shopping_policy_on_items(item_name, conditions, restrict, quantity):
    if item_name is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if quantity < 0:
                return "FAILED: Negative quantity is invalid."
            return ShoppingPolicies.add_shopping_policy_on_items(item_name, conditions, restrict, quantity)
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_category(category, conditions, restrict, quantity):
    if category is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if quantity < 0:
                return "FAILED: Negative quantity is invalid."
            return ShoppingPolicies.add_shopping_policy_on_category(category, conditions, restrict, quantity)
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_shop(shop_name, conditions, restrict, quantity):
    if shop_name is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if quantity < 0:
                return "FAILED: Negative quantity is invalid."
            return ShoppingPolicies.add_shopping_policy_on_shop(shop_name, conditions, restrict, quantity)
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_identity(conditions, restrict, quantity):
    if conditions is not None and restrict is not None and quantity is not None:
        if quantity < 0:
            return "FAILED: Negative quantity is invalid."
        return ShoppingPolicies.add_shopping_policy_on_identity(conditions, restrict, quantity)
    return "FAILED: One (or more) of the parameters is None"


#    ____________________________________   DELETE     ___________________________________________________


def remove_shopping_policy_on_identity(policy_id):
    if policy_id is not None and policy_id > 0:
        return ShoppingPolicies.remove_shopping_policy_on_identity(policy_id)
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_shop(policy_id):
    if policy_id is not None and policy_id > 0:
        return ShoppingPolicies.remove_shopping_policy_on_shop(policy_id)
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_items(policy_id):
    if policy_id is not None and policy_id > 0:
        return ShoppingPolicies.remove_shopping_policy_on_items(policy_id)
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_category(policy_id):
    if policy_id is not None and policy_id > 0:
        return ShoppingPolicies.remove_shopping_policy_on_category(policy_id)
    return "FAILED: Invalid id of Policy"


#    ____________________________________   UPDATE     ___________________________________________________


def update_shopping_policy_on_identity(policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        return ShoppingPolicies.update_shopping_policy_on_identity(policy_id, field_name, new_value)
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_shop(policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['shop_name', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        return ShoppingPolicies.update_shopping_policy_on_shop(policy_id, field_name, new_value)
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_items(policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['item_name', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        return ShoppingPolicies.update_shopping_policy_on_items(policy_id, field_name, new_value)
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_category(policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['category', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        return ShoppingPolicies.update_shopping_policy_on_category(policy_id, field_name, new_value)
    return "FAILED: One (or more) of the parameters is None"
