from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.LogTuple import ErrorTuple, EventTuple, LoginTuple


#    ______ ______ _______ _____ _    _ ______ _____   _____
#   |  ____|  ____|__   __/ ____| |  | |  ____|  __ \ / ____|
#   | |__  | |__     | | | |    | |__| | |__  | |__) | (___
#   |  __| |  __|    | | | |    |  __  |  __| |  _  / \___ \
#   | |    | |____   | | | |____| |  | | |____| | \ \ ____) |
#   |_|    |______|  |_|  \_____|_|  |_|______|_|  \_\_____/
#
#


def fetch_event_tuples(results):
    array = []
    for item in results:
        array.append(EventTuple(item[0], item[1], item[2]))
    return array


def fetch_error_tuples(results):
    array = []
    for item in results:
        array.append(ErrorTuple(item[0], item[1], item[2], item[3]))
    return array


def fetch_login_tuples(results):
    array = []
    for item in results:
        array.append(LoginTuple(item[0], item[1]))
    return array


#    ________      ________ _   _ _______   _      ____   _____  _____
#   |  ____\ \    / /  ____| \ | |__   __| | |    / __ \ / ____|/ ____|
#   | |__   \ \  / /| |__  |  \| |  | |    | |   | |  | | |  __| (___
#   |  __|   \ \/ / |  __| | . ` |  | |    | |   | |  | | | |_ |\___ \
#   | |____   \  /  | |____| |\  |  | |    | |___| |__| | |__| |____) |
#   |______|   \/   |______|_| \_|  |_|    |______\____/ \_____|_____/
#
#


def add_event_log(tuple_log):
    sql_query = """
            INSERT INTO Event_Logs (username, time, event)  
            VALUES ('{}', '{}', '{}');
          """.format(tuple_log.username, tuple_log.time, tuple_log.event)
    return commit_command(sql_query)


def get_event_logs_by_event(event):
    sql_query = """
            SELECT * FROM Event_Logs WHERE event = '{}'
        """.format(event)
    return fetch_event_tuples(select_command(sql_query))


def get_all_event_logs():
    sql_query = """ SELECT * FROM Event_Logs """
    return fetch_event_tuples(select_command(sql_query))


#    ______ _____  _____   ____  _____    _      ____   _____  _____
#   |  ____|  __ \|  __ \ / __ \|  __ \  | |    / __ \ / ____|/ ____|
#   | |__  | |__) | |__) | |  | | |__) | | |   | |  | | |  __| (___
#   |  __| |  _  /|  _  /| |  | |  _  /  | |   | |  | | | |_ |\___ \
#   | |____| | \ \| | \ \| |__| | | \ \  | |___| |__| | |__| |____) |
#   |______|_|  \_\_|  \_\\____/|_|  \_\ |______\____/ \_____|_____/
#
#

def add_error_log(tuple_log):
    sql_query = """
            INSERT INTO Error_Logs (username, time, event, additional_details)  
            VALUES ('{}', '{}', '{}', '{}');
          """.format(tuple_log.username, tuple_log.time, tuple_log.event, tuple_log.additional_details)
    return commit_command(sql_query)


def get_error_logs_by_event(event):
    sql_query = """
            SELECT * FROM Error_Logs WHERE event = '{}'
        """.format(event)
    return fetch_error_tuples(select_command(sql_query))


def get_all_error_logs():
    sql_query = """ SELECT * FROM Error_Logs """
    return fetch_error_tuples(select_command(sql_query))


#    _      ____   _____ _____ _   _     _      ____   _____  _____
#   | |    / __ \ / ____|_   _| \ | |   | |    / __ \ / ____|/ ____|
#   | |   | |  | | |  __  | | |  \| |   | |   | |  | | |  __| (___
#   | |   | |  | | | |_ | | | | . ` |   | |   | |  | | | |_ |\___ \
#   | |___| |__| | |__| |_| |_| |\  |   | |___| |__| | |__| |____) |
#   |______\____/ \_____|_____|_| \_|   |______\____/ \_____|_____/
#
#

def add_login_log(tuple_log):
    sql_query = """
            INSERT INTO Login_Logs (username, time)  
            VALUES ('{}', '{}');
          """.format(tuple_log.username, tuple_log.time)
    return commit_command(sql_query)


def get_all_login_logs():
    sql_query = """ SELECT * FROM Login_Logs """
    return fetch_login_tuples(select_command(sql_query))
