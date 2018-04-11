from DatabaseLayer import Messages, StoreManagers


def send_message(message_from, message_to, content):
    if message_from is not None and message_to is not None and content is not None:
        return Messages.send_message(message_from, message_to, content)


def get_all_messages(username):
    if username is not None:
        return Messages.get_all_messages(username)


def get_all_shop_messages(username, shop_name):
    manager = StoreManagers.getStoreManager(username, shop_name)
    if manager is not False:
        get_all_shop_messages_permission = manager[6]
        if get_all_shop_messages_permission > 0:
            return Messages.get_all_shop_messages(shop_name)

    return False


def send_message_from_shop(username, message, shop_name, to):
    manager = StoreManagers.getStoreManager(username, shop_name)
    if manager is not False:
        reply_message_permission = manager[5]
        if reply_message_permission > 0:
            Messages.send_message_from_shop(message, shop_name, to)

    return False
