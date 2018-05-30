from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.HistoryAppointing import HistoryAppointing


def fetch_history_appointings(results):
    array = []
    for history_appointing in results:
        array.append(HistoryAppointing(history_appointing[1], history_appointing[2], history_appointing[3], history_appointing[4], history_appointing[5], history_appointing[6]))
    return array


def add_history_appointing(appointing_user, appointed_user, position, shop_name, date, permissions):
    sql_query = """
                INSERT INTO HistoryOfAppointing (appointingUser, appointedUser, position, shop_name, date, permissions)
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
              """.format(appointing_user, appointed_user, position, shop_name, date, permissions)
    return commit_command(sql_query)


def update_history_appointing(appointing_user, appointed_user, shop_name, permissions):
    sql_query = """
                UPDATE HistoryOfAppointing SET permissions = '{}'
                WHERE appointingUser='{}' AND appointedUser='{}' AND shop_name='{}' 
              """.format(permissions, appointing_user, appointed_user, shop_name)
    return commit_command(sql_query)


def get_history_appointing_by_shop(shop_name):
    sql_query = """
                    SELECT *
                    FROM HistoryOfAppointing
                    WHERE shop_name = '{}'
                  """.format(shop_name)
    return fetch_history_appointings(select_command(sql_query))