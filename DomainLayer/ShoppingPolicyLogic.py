from DatabaseLayer import ShoppingPolicies
from DatabaseLayer import SystemManagers
from DatabaseLayer import Owners

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


def add_shopping_policy_on_items(username, item_name, conditions, restrict, quantity):
    if item_name is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if restrict not in ['N', 'AL', 'E', 'UT']:
                return "FAILED: Invalid value of restrict."
            if quantity < 0:
                return "FAILED: Negative quantity is invalid."
            if SystemManagers.is_system_manager(username) is not False:
                if not ShoppingPolicies.add_shopping_policy_on_items(item_name, conditions, restrict, quantity):
                    return "FAILED: DB error."
                return True
            return 'FAILED: you are not a System Manager'
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_category(username, category, conditions, restrict, quantity):
    if category is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if restrict not in ['N', 'AL', 'E', 'UT']:
                return "FAILED: Invalid value of restrict."
            if quantity < 0:
                return "FAILED: Negative quantity is invalid."
            if SystemManagers.is_system_manager(username) is not False:
                if not ShoppingPolicies.add_shopping_policy_on_category(category, conditions, restrict, quantity):
                    return "FAILED: DB error."
                return True
            return 'FAILED: you are not a System Manager'
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_shop(username, shop_name, conditions, restrict, quantity):
    if shop_name is not None and conditions is not None:
        if restrict is not None and quantity is not None:
            if restrict not in ['N', 'AL', 'E', 'UT']:
                return "FAILED: Invalid value of restrict."
            if quantity < 0:
                return "FAILED: Negative quantity is invalid."
            if Owners.get_owner(username, shop_name) is not False:
                if not ShoppingPolicies.add_shopping_policy_on_shop(shop_name, conditions, restrict, quantity):
                    return "FAILED: DB error."
                return True
            return 'FAILED: you are not a the Owner of the shop'
        return "FAILED: One (or more) of the parameters is None"
    return "FAILED: One (or more) of the parameters is None"


def add_shopping_policy_on_identity(username, conditions, restrict, quantity):
    if conditions is not None and restrict is not None and quantity is not None:
        if restrict not in ['N', 'AL', 'E', 'UT']:
            return "FAILED: Invalid value of restrict."
        if quantity < 0:
            return "FAILED: Negative quantity is invalid."
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.add_shopping_policy_on_identity(conditions, restrict, quantity):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


#    ____________________________________   DELETE     ___________________________________________________


def remove_shopping_policy_on_identity(username, policy_id):
    if policy_id is not None and policy_id > 0:
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_identity(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_shop(username, policy_id, shop_name):
    if policy_id is not None and policy_id > 0:
        if Owners.get_owner(username, shop_name) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_shop(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a the Owner of the shop'
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_items(username, policy_id):
    if policy_id is not None and policy_id > 0:
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_items(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: Invalid id of Policy"


def remove_shopping_policy_on_category(username, policy_id):
    if policy_id is not None and policy_id > 0:
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.remove_shopping_policy_on_category(policy_id):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: Invalid id of Policy"


#    ____________________________________   UPDATE     ___________________________________________________


def update_shopping_policy_on_identity(username, policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.update_shopping_policy_on_identity(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_shop(username, policy_id, field_name, new_value, shop_name):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['shop_name', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if Owners.get_owner(username, shop_name) is not False:
            if not ShoppingPolicies.update_shopping_policy_on_shop(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a the Owner of the shop'
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_items(username, policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['item_name', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.update_shopping_policy_on_items(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"


def update_shopping_policy_on_category(username, policy_id, field_name, new_value):
    if policy_id is not None and field_name is not None and new_value is not None:
        if policy_id < 0:
            return "FAILED: Invalid id of Policy"
        if field_name not in ['category', 'conditions', 'restrict', 'quantity']:
            return "FAILED: Invalid field name"
        if SystemManagers.is_system_manager(username) is not False:
            if not ShoppingPolicies.update_shopping_policy_on_category(policy_id, field_name, new_value):
                return "FAILED: DB error."
            return True
        return 'FAILED: you are not a System Manager'
    return "FAILED: One (or more) of the parameters is None"
