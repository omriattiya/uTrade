from DatabaseLayer.getConn import commit_command, select_command
from datetime import datetime
from SharedClasses.VisibleDiscount import VisibleDiscount
from SharedClasses.InvisibleDiscount import InvisibleDiscount
from datetime import date


def fetch_discount(discount_tuples):
    if discount_tuples is False:
        return False
    if len(discount_tuples) == 0:
        return False
    discounts_arr = []
    for discount_tuple in discount_tuples:
        if len(discount_tuple) == 5:
            discounts_arr.append(VisibleDiscount(discount_tuple[0],
                                                 discount_tuple[1],
                                                 discount_tuple[2],
                                                 discount_tuple[3],
                                                 discount_tuple[4]))
        else:
            discounts_arr.append(InvisibleDiscount(discount_tuple[0],
                                                   discount_tuple[1],
                                                   discount_tuple[2],
                                                   discount_tuple[3],
                                                   discount_tuple[4],
                                                   discount_tuple[5]))
    return discounts_arr


def add_visible_discount(visible_discount):
    sql_query = """
                INSERT INTO VisibleDiscounts (item_id, shop_name, percentage, from_date, end_date)  
                VALUES ('{}', '{}', '{}', '{}', '{}');
              """.format(visible_discount.item_id, visible_discount.shop_name,
                         visible_discount.percentage,
                         visible_discount.from_date, visible_discount.end_date)
    return commit_command(sql_query)


def add_invisible_discount(invisible_discount):
    sql_query = """
                INSERT INTO InvisibleDiscounts (item_id, shop_name, percentage, from_date, end_date, code)  
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
              """.format(invisible_discount.item_id,
                         invisible_discount.shop_name,
                         invisible_discount.percentage,
                         invisible_discount.from_date,
                         invisible_discount.end_date,
                         invisible_discount.code)
    return commit_command(sql_query)


def get_visible_discount(item_id, shop_name):
    sql_query = """
                SELECT *
                FROM VisibleDiscounts
                WHERE item_id = '{}' AND 
                      shop_name = '{}'
              """.format(item_id, shop_name)
    return fetch_discount(select_command(sql_query))


def get_invisible_discount(item_id, shop_name, text):
    sql_query = """
                SELECT *
                FROM InvisibleDiscounts
                WHERE item_id = '{}' AND 
                      shop_name = '{}' AND 
                      '{}' = code
              """.format(item_id, shop_name, text)
    return fetch_discount(select_command(sql_query))

