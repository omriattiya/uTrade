from time import gmtime, strftime

from DatabaseLayer import Logger
from SharedClasses.LogTuple import ErrorTuple, EventTuple, LoginTuple, SecurityTuple


def now_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())


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
