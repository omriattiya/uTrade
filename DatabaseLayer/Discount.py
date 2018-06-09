from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.InvisibleDiscount import InvisibleDiscount
from SharedClasses.InvisibleDiscountCategory import InvisibleDiscountCategory
from SharedClasses.VisibleDiscount import VisibleDiscount
from SharedClasses.VisibleDiscountCategory import VisibleDiscountCategory


def fetch_discount_item(discount_tuples):
    if discount_tuples is False:
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


def fetch_discount_category(discount_tuples):
    if discount_tuples is False:
        return False
    discounts_arr = []
    for discount_tuple in discount_tuples:
        if len(discount_tuple) == 5:
            discounts_arr.append(VisibleDiscountCategory(discount_tuple[0],
                                                         discount_tuple[1],
                                                         discount_tuple[2],
                                                         discount_tuple[3],
                                                         discount_tuple[4]))
        else:
            discounts_arr.append(InvisibleDiscountCategory(discount_tuple[0],
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
    return fetch_discount_item(select_command(sql_query))


def get_invisible_discount(item_id, shop_name, text):
    sql_query = """
                SELECT *
                FROM InvisibleDiscounts
                WHERE item_id = '{}' AND 
                      shop_name = '{}' AND 
                      '{}' = code
              """.format(item_id, shop_name, text)
    return fetch_discount_item(select_command(sql_query))


def get_all_visible_item(shop_name):
    sql_query = """
                  SELECT *
                  FROM VisibleDiscounts
                  WHERE shop_name = '{}'
                """.format(shop_name)
    return fetch_discount_item(select_command(sql_query))


def get_all_invisible_item(shop_name):
    sql_query = """
                  SELECT *
                  FROM InvisibleDiscounts
                  WHERE shop_name = '{}'
                """.format(shop_name)
    return fetch_discount_item(select_command(sql_query))


def delete_visible_item_discount(item_id, shop_name, from_date):
    sql_query = """
                DELETE FROM VisibleDiscounts
                WHERE item_id={} AND shop_name = '{}' AND from_date='{}'
              """.format(item_id, shop_name, from_date)
    return commit_command(sql_query)


def delete_invisible_item_discount(item_id, shop_name, from_date, code):
    sql_query = """
                DELETE FROM InvisibleDiscounts
                WHERE item_id={} AND shop_name = '{}' AND from_date='{}' AND code='{}'
              """.format(item_id, shop_name, from_date, code)
    return commit_command(sql_query)

# ___________________________________________ CATEGORY __________________________________________________________


def add_visible_discount_category(visible_discount):
    sql_query = """
                INSERT INTO VisibleDiscountsCategory (category, shop_name, percentage, from_date, end_date)  
                VALUES ('{}', '{}', '{}', '{}', '{}');
              """.format(visible_discount.category, visible_discount.shop_name,
                         visible_discount.percentage,
                         visible_discount.from_date, visible_discount.end_date)
    return commit_command(sql_query)


def add_invisible_discount_category(invisible_discount):
    sql_query = """
                INSERT INTO InvisibleDiscountsCategory (category, shop_name, percentage, from_date, end_date, code)  
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
              """.format(invisible_discount.category,
                         invisible_discount.shop_name,
                         invisible_discount.percentage,
                         invisible_discount.from_date,
                         invisible_discount.end_date,
                         invisible_discount.code)
    return commit_command(sql_query)


def get_visible_discount_category(category, shop_name):
    sql_query = """
                SELECT *
                FROM VisibleDiscountsCategory
                WHERE category = '{}' AND 
                      shop_name = '{}'
              """.format(category, shop_name)
    return fetch_discount_category(select_command(sql_query))


def get_invisible_discount_category(category, shop_name, text):
    sql_query = """
                SELECT *
                FROM InvisibleDiscountsCategory
                WHERE category = '{}' AND 
                      shop_name = '{}' AND 
                      '{}' = code
              """.format(category, shop_name, text)
    return fetch_discount_category(select_command(sql_query))


def get_all_visible_category(shop_name):
    sql_query = """
                SELECT *
                FROM VisibleDiscountsCategory
                WHERE shop_name = '{}'
              """.format(shop_name)
    return fetch_discount_category(select_command(sql_query))


def get_all_invisible_category(shop_name):
    sql_query = """
                SELECT *
                FROM InvisibleDiscountsCategory
                WHERE shop_name = '{}'
              """.format(shop_name)
    return fetch_discount_category(select_command(sql_query))


def delete_visible_category_discount(category, shop_name, from_date):
    sql_query = """
                    DELETE FROM VisibleDiscountsCategory
                    WHERE category='{}' AND shop_name = '{}' AND from_date='{}'
                  """.format(category, shop_name, from_date)
    return commit_command(sql_query)


def delete_invisible_category_discount(category, shop_name, from_date, code):
    sql_query = """
                    DELETE FROM InvisibleDiscountsCategory
                    WHERE category='{}' AND shop_name = '{}' AND from_date='{}' AND code='{}'
                  """.format(category, shop_name, from_date, code)
    return commit_command(sql_query)
