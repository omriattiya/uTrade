from DatabaseLayer.getConn import select_command, commit_command
from SharedClasses.ShoppingPolicyOnIdentity import ShoppingPolicyOnIdentity
from SharedClasses.ShoppingPolicyOnItems import ShoppingPolicyOnItems
from SharedClasses.ShoppingPolicyOnShop import ShoppingPolicyOnShop
from SharedClasses.ShoppingPolicyOnCategory import ShoppingPolicyOnCategory


#    ____________________________________   FETCH MANY     ___________________________________________________


def fetch_shopping_policies_on_identity(results):
    array = []
    for item in results:
        array.append(ShoppingPolicyOnIdentity(item[0], item[1], item[2], item[3]))
    return array


def fetch_shopping_policies_on_items(results):
    array = []
    for item in results:
        array.append(ShoppingPolicyOnItems(item[0], item[1], item[2], item[3], item[4]))
    return array


def fetch_shopping_policies_on_category(results):
    array = []
    for item in results:
        array.append(ShoppingPolicyOnCategory(item[0], item[1], item[2], item[3], item[4]))
    return array


def fetch_shopping_policies_on_shop(results):
    array = []
    for item in results:
        array.append(ShoppingPolicyOnShop(item[0], item[1], item[2], item[3], item[4]))
    return array


#    ____________________________________   FETCH ONE     ___________________________________________________


def fetch_shopping_policy_on_identity(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ShoppingPolicyOnIdentity(result[0], result[1], result[2], result[3])


def fetch_shopping_policy_on_category(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ShoppingPolicyOnCategory(result[0], result[1], result[2], result[3], result[4])


def fetch_shopping_policy_on_items(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ShoppingPolicyOnItems(result[0], result[1], result[2], result[3], result[4])


def fetch_shopping_policy_on_shops(result):
    if len(result) == 0:
        return False
    result = result[0]
    return ShoppingPolicyOnShop(result[0], result[1], result[2], result[3], result[4])


#    ____________________________________   GET ALL     ___________________________________________________


def get_all_shopping_policy_on_shop(shop_name):
    sql_query = """
                SELECT *
               FROM ShoppingPolicyOnShop
               WHERE shop_name='{}'
              """.format(shop_name)
    return fetch_shopping_policies_on_shop(select_command(sql_query))


def get_all_shopping_policy_on_items():
    sql_query = """
                SELECT *
               FROM ShoppingPolicyOnItems
              """
    return fetch_shopping_policies_on_items(select_command(sql_query))


def get_all_shopping_policy_on_category():
    sql_query = """
                SELECT *
               FROM ShoppingPolicyOnCategory
              """
    return fetch_shopping_policies_on_category(select_command(sql_query))


def get_all_shopping_policy_on_identity():
    sql_query = """
                SELECT *
               FROM ShoppingPolicyOnIdentity
              """
    return fetch_shopping_policies_on_identity(select_command(sql_query))


#    ____________________________________   INSERT     ___________________________________________________


def add_shopping_policy_on_items(item_name, conditions, restriction, quantity):
    sql_query = """
                INSERT INTO ShoppingPolicyOnItems(item_name, conditions, restriction, quantity)
                VALUES ('{}','{}','{}','{}')
                """.format(item_name, conditions, restriction, quantity)
    return commit_command(sql_query)


def add_shopping_policy_on_category(category, conditions, restriction, quantity):
    sql_query = """
                INSERT INTO ShoppingPolicyOnCategory(category, conditions, restriction, quantity)
                VALUES ('{}','{}','{}','{}')
                """.format(category, conditions, restriction, quantity)
    return commit_command(sql_query)


def add_shopping_policy_on_shop(shop_name, conditions, restriction, quantity):
    sql_query = """
                INSERT INTO ShoppingPolicyOnShop(shop_name, conditions, restriction, quantity)
                VALUES ('{}','{}','{}','{}')
                """.format(shop_name, conditions, restriction, quantity)
    return commit_command(sql_query)


def add_shopping_policy_on_identity(conditions, restriction, quantity):
    sql_query = """
                INSERT INTO ShoppingPolicyOnIdentity(conditions, restriction, quantity)
                VALUES ('{}','{}','{}')
                """.format(conditions, restriction, quantity)
    return commit_command(sql_query)


#    ____________________________________   DELETE     ___________________________________________________


def remove_shopping_policy_on_identity(policy_id):
    sql = """
                DELETE FROM ShoppingPolicyOnIdentity
                WHERE policy_id = '{}'
              """.format(policy_id)
    return commit_command(sql)


def remove_shopping_policy_on_shop(policy_id):
    sql = """
                DELETE FROM ShoppingPolicyOnShop
                WHERE policy_id = '{}'
              """.format(policy_id)
    return commit_command(sql)


def remove_shopping_policy_on_items(policy_id):
    sql = """
                DELETE FROM ShoppingPolicyOnItems
                WHERE policy_id = '{}'
              """.format(policy_id)
    return commit_command(sql)


def remove_shopping_policy_on_category(policy_id):
    sql = """
                DELETE FROM ShoppingPolicyOnCategory
                WHERE policy_id = '{}'
              """.format(policy_id)
    return commit_command(sql)


#    ____________________________________   UPDATE     ___________________________________________________


def update_shopping_policy_on_identity(policy_id, field_name, new_value):
    sql = """
            UPDATE ShoppingPolicyOnIdentity
            SET {} = '{}'
            WHERE policy_id = '{}'
            """.format(field_name, new_value, policy_id)
    return commit_command(sql)


def update_shopping_policy_on_shop(policy_id, field_name, new_value):
    sql = """
            UPDATE ShoppingPolicyOnShop
            SET {} = '{}'
            WHERE policy_id = '{}'
            """.format(field_name, new_value, policy_id)
    return commit_command(sql)


def update_shopping_policy_on_items(policy_id, field_name, new_value):
    sql = """
            UPDATE ShoppingPolicyOnItems
            SET {} = '{}'
            WHERE policy_id = '{}'
            """.format(field_name, new_value, policy_id)
    return commit_command(sql)


def update_shopping_policy_on_category(policy_id, field_name, new_value):
    sql = """
            UPDATE ShoppingPolicyOnCategory
            SET {} = '{}'
            WHERE policy_id = '{}'
            """.format(field_name, new_value, policy_id)
    return commit_command(sql)
