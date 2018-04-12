from DatabaseLayer.getConn import commit_command, select_command
from datetime import datetime


def add_visible_discount(visible_discount):
    sql_query = """
                INSERT INTO VisibleDiscounts (item_id, shop_name, percentage, from_date, end_date)  
                VALUES ('{}', '{}', '{}', '{}', '{}');
              """.format(visible_discount.discount_id,
                         visible_discount.item_id, visible_discount.shop_name,
                         visible_discount.percentage,
                         visible_discount.from_date, visible_discount.end_date)
    return commit_command(sql_query)


def add_invisible_discount(invisible_discount):
    sql_query = """
                INSERT INTO InvisibleDiscounts (item_id, shop_name, percentage, from_date, end_date, code)  
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
              """.format(invisible_discount.discount_id,
                         invisible_discount.item_id,
                         invisible_discount.shop_name,
                         invisible_discount.percentage,
                         invisible_discount.from_date,
                         invisible_discount.end_date,
                         invisible_discount.code)
    return commit_command(sql_query)


def get_visible_discount(item_id, shop_name):
    now = datetime.now()
    sql_query = """
                SELECT percentage
                FROM VisibleDiscounts
                WHERE item_id = '{}' AND 
                      shop_name = '{}' AND 
                      '{}' >= from_date AND 
                      '{}' <= end_date
              """.format(item_id, shop_name, now, now)
    return select_command(sql_query)


def get_invisible_discount(item_id, shop_name, text):
    now = datetime.now()
    sql_query = """
                SELECT percentage
                FROM InvisibleDiscounts
                WHERE item_id = '{}' AND 
                      shop_name = '{}' AND 
                      '{}' >= from_date AND 
                      '{}' <= end_date AND
                      '{}' = code
              """.format(item_id, shop_name, now, now, text)
    return select_command(sql_query)

