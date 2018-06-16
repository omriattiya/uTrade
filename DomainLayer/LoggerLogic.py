import datetime

from DatabaseLayer import Logger
from SharedClasses.LogTuple import ErrorTuple, EventTuple, LoginTuple, SecurityTuple


def now_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


#             _____  _____  ______ _____   _____
#       /\   |  __ \|  __ \|  ____|  __ \ / ____|
#      /  \  | |  | | |  | | |__  | |__) | (___
#     / /\ \ | |  | | |  | |  __| |  _  / \___ \
#    / ____ \| |__| | |__| | |____| | \ \ ____) |
#   /_/    \_\_____/|_____/|______|_|  \_\_____/
#
#

def add_event_log(username, event):
    return Logger.add_event_log(EventTuple(username, now_time(), event))


def add_error_log(username, event, additional_details):
    return Logger.add_error_log(ErrorTuple(username, now_time(), event, additional_details))


def add_login_log(username):
    return Logger.add_login_log(LoginTuple(username, now_time()))


def add_security_log(event, additional_details):
    return Logger.add_security_log(SecurityTuple(now_time(), event, additional_details))


#      _____ ______ _______ _______ ______ _____   _____
#    / ____|  ____|__   __|__   __|  ____|  __ \ / ____|
#   | |  __| |__     | |     | |  | |__  | |__) | (___
#   | | |_ |  __|    | |     | |  |  __| |  _  / \___ \
#   | |__| | |____   | |     | |  | |____| | \ \ ____) |
#    \_____|______|  |_|     |_|  |______|_|  \_\_____/
#
#


def get_all_event_logs():
    return Logger.get_all_event_logs()


def get_all_error_logs():
    return Logger.get_all_error_logs()


def get_all_login_logs():
    return Logger.get_all_login_logs()


def get_all_security_logs():
    return Logger.get_all_security_logs()


#     _____ ______ _______ _______ ______ _____   _____   ______     __
#    / ____|  ____|__   __|__   __|  ____|  __ \ / ____| |  _ \ \   / /
#   | |  __| |__     | |     | |  | |__  | |__) | (___   | |_) \ \_/ /
#   | | |_ |  __|    | |     | |  |  __| |  _  / \___ \  |  _ < \   /
#   | |__| | |____   | |     | |  | |____| | \ \ ____) | | |_) | | |
#    \_____|______|  |_|     |_|  |______|_|  \_\_____/  |____/  |_|
#
#


def get_event_logs_by_event(event):
    return Logger.get_event_logs_by_event(event)


def get_error_logs_by_event(event):
    return Logger.get_error_logs_by_event(event)


def check_injection(original_input, substring, event, code):
    if original_input.lower().count(substring.lower()) > 0:
        original_input = original_input.lower().replace(substring, "" + code)
        add_security_log(event, "INPUT CONTAINS INJECTION WITH CODE:" + code + " ORIGIN: " + original_input)
        return True
    return False


def identify_sql_injection(original_input, event):
    is_suspected = False
    # TAKEN FROM :  https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/
    cheat_sheet = ["'", "--", "#", "1/0", "IF(", "0x", "||", "CONCAT", "LOAD_FILE", "CHAR", "ASCII", "Hex", "MD5",
                   "ORDER BY", "INSERT INTO", "LIMIT", "UNION", "BENCHMARK", "sleep(", "DELETE", "DROP"]
    i = 0
    for substring in cheat_sheet:
        is_suspected = check_injection(original_input, substring, event, str(i)) or is_suspected
        i = i + 1
    return is_suspected


MESSAGE_SQL_INJECTION = "FAIL: suspect sql injection"
