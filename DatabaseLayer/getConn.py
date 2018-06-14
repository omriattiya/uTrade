import sqlite3
import os
from sqlite3 import Error
from django.db import connection


# if len(os.environ) > 3:
#  if os.environ.get('test_flag') == "True":


def get_conn():
    if os.environ.get('test_flag') is None or os.environ.get('test_flag') == "True":
        if os.environ.get('test_flag') is None:
            conn = sqlite3.connect('../../db.sqlite3')
        elif os.environ.get('test_flag') == "True":
            conn = sqlite3.connect('db.sqlite3')
        conn.execute("""
                              PRAGMA foreign_keys = ON
                      """)
        return conn
    else:
        return connection


def commit_command(sql_query):
    conn = get_conn()
    try:
        conn.cursor().execute(sql_query)
        conn.commit()
        conn.close()
        return True
    except Error as e:
        conn.close()
        return False


def select_command(sql_query):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute(sql_query)
        results = c.fetchall()
        conn.close()
        return results
    except Error as e:
        print(e)
        conn.close()
        return []


def delete_content():
    delete_sql_texts = []
    delete_sql_texts.append("DELETE FROM CustomersInLotteries")
    delete_sql_texts.append("DELETE FROM GlobalDiscountInShop")
    delete_sql_texts.append("DELETE FROM HistoryOfAppointing")
    delete_sql_texts.append("DELETE FROM InvisibleDiscounts")
    delete_sql_texts.append("DELETE FROM InvisibleDiscountsCategory")
    delete_sql_texts.append("DELETE FROM Items")
    delete_sql_texts.append("DELETE FROM Lotteries")
    delete_sql_texts.append("DELETE FROM Messages")
    delete_sql_texts.append("DELETE FROM Owners")
    delete_sql_texts.append("DELETE FROM PurchasePolicy")
    delete_sql_texts.append("DELETE FROM PurchasedItems")
    delete_sql_texts.append("DELETE FROM Purchases")
    delete_sql_texts.append("DELETE FROM RegisteredUsers")
    delete_sql_texts.append("DELETE FROM ReviewsOnItems")
    delete_sql_texts.append("DELETE FROM ReviewsOnShops")
    delete_sql_texts.append("DELETE FROM ShoppingCartItem")
    delete_sql_texts.append("DELETE FROM ShoppingPolicyOnCategory")
    delete_sql_texts.append("DELETE FROM ShoppingPolicyOnIdentity")
    delete_sql_texts.append("DELETE FROM ShoppingPolicyOnItems")
    delete_sql_texts.append("DELETE FROM ShoppingPolicyOnShop")
    delete_sql_texts.append("DELETE FROM Shops")
    delete_sql_texts.append("DELETE FROM StoreManagers")
    delete_sql_texts.append("DELETE FROM SystemManagers")
    delete_sql_texts.append("DELETE FROM UserDetails")
    delete_sql_texts.append("DELETE FROM VisibleDiscounts")
    delete_sql_texts.append("DELETE FROM VisibleDiscountsCategory")

    for sql_text in delete_sql_texts:
        commit_command(sql_text)
