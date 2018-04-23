from DatabaseLayer import Messages, StoreManagers, Owners, Shops
from SharedClasses import Message
from DatabaseLayer.RegisteredUsers import get_user


def send_message(message):
    if message.from_username is not None and message.to_username is not None and message.content is not None:
        if get_user(message.from_username) is not False:
            if get_user(message.to_username) is not False:
                return Messages.send_message(message)


def get_all_messages(username):
    if username is not None:
        if get_user(username) is not False:
            return Messages.get_all_messages(username)


def get_all_shop_messages(username, shop_name):
    manager = StoreManagers.get_store_manager(username, shop_name)
    if manager is not False:
        if manager.permission_get_all_messages > 0:
            if Shops.search_shop(shop_name) is not False:
                return Messages.get_all_shop_messages(shop_name)
    if Owners.get_owner(username, shop_name) is not False:
        if Shops.search_shop(shop_name) is not False:
            return Messages.get_all_shop_messages(shop_name)
    return False


def send_message_from_shop(username, message):
    manager = StoreManagers.get_store_manager(username, message.from_username)
    if manager is not False:
        if manager.permission_reply_messages > 0:
            if Shops.search_shop(message.to_username) is not False:
                if Shops.search_shop(message.from_username) is not False:
                    Messages.send_message_from_shop(message)
    if Owners.get_owner(username, message.from_username) is not False:
        if Shops.search_shop(message.to_username) is not False:
            if Shops.search_shop(message.from_username) is not False:
                Messages.send_message_from_shop(message)
    return False
