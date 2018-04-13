from DatabaseLayer import Messages, StoreManagers
from SharedClasses import Message


def send_message(message):
    if message.from_username is not None and message.to_username is not None and message.content is not None:
        return Messages.send_message(message)


def get_all_messages(username):
    if username is not None:
        return Messages.get_all_messages(username)


def get_all_shop_messages(username, shop_name):
    manager = StoreManagers.get_store_manager(username, shop_name)
    if manager is not False:
        if manager.permission_get_all_messages > 0:
            return Messages.get_all_shop_messages(shop_name)

    return False


def send_message_from_shop(username, message):
    manager = StoreManagers.get_store_manager(username, message.from_username)
    if manager is not False:
        if manager.permission_reply_messages > 0:
            Messages.send_message_from_shop(message)

    return False
