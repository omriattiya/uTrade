from DatabaseLayer.getConn import select_command, commit_command, get_conn
from SharedClasses.Purchase import Purchase
from sqlite3 import Error


def fetch_purchases(results):
    array = []
    for purchase in results:
        array.append(Purchase(purchase[0], purchase[1], purchase[2], purchase[3]))
    return array


def fetch_purchase(result):
    array = []
    for purchase in result:
        array.append(Purchase(purchase[0], purchase[1], purchase[2], purchase[3]))
    return array[0]


def add_purchase_and_return_id(purchase_date, username, total_price):
    sql_query = """
                    INSERT INTO Purchases(purchaseDate,username,totalPrice)
                    VALUES ('{}','{}','{}')
                    """.format(purchase_date, username, total_price)
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute(sql_query)
        conn.commit()
        to_return = c.lastrowid
        conn.close()
        return to_return
    except Error as e:
        return False


def get_user_purchases(username):
    sql_query = """
                   SELECT *
                  FROM Purchases
                  WHERE username = '{}'
                 """.format(username)
    return fetch_purchases(select_command(sql_query))


def update_purchase_total_price(purchase_id, total_price):
    sql_query = """
                UPDATE Purchases SET totalPrice = {}
                WHERE purchaseId = {}
                """.format(total_price, purchase_id)
    return commit_command(sql_query)


def get_purchase(purchase_id):
    sql_query = """
                       SELECT *
                      FROM Purchases
                      WHERE purchaseId = '{}'
                     """.format(purchase_id)
    return fetch_purchase(select_command(sql_query))
