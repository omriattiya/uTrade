from DatabaseLayer import Messages, StoreManagers, Owners, Shops, SystemManagers, RegisteredUsers
from DatabaseLayer.RegisteredUsers import get_user
from DomainLayer import LoggerLogic
from ServiceLayer.services.LiveAlerts import MessagingAlerts


def send_message(message):
    if message.from_username is not None and message.to_username is not None and message.content is not None:
        if message.to_username == 'System' or get_user(message.to_username) is not False or Shops.search_shop(
                message.to_username) is not False:
            # output = Messages.send_message(message)

            if SystemManagers.is_system_manager(message.from_username):
                message.from_username = 'System'
            output = Messages.send_message(message)
        else:
            return "FAILED: Target user is incorrect"
    else:
        return "FAILED: Missing Parameters"
    if output:
        users = [message.to_username]
        if message.to_username == 'System':
            LoggerLogic.add_event_log(message.from_username, "REPORT ITEM / SHOP")
            SMs = SystemManagers.get_all_system_managers()
            SM_names = []
            for sm in SMs:
                SM_names.append(sm.username)
            users = SM_names
        MessagingAlerts.notify_messaging_alerts(users,
                                                '<a href = "../app/home/messages/?content=received" > '
                                                'You Have a new message from ' + message.from_username + '</a>')
        return "SUCCESS"
    else:
        return "FAILED"


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
    output = False
    manager = StoreManagers.get_store_manager(username, message.from_username)
    if Shops.search_shop(message.to_username) is False and RegisteredUsers.is_user_exists(
            message.to_username) is False:
        return "FAILED: Target does not exists"
    if manager is not False:
        if manager.permission_reply_messages > 0:
            output = Messages.send_message_from_shop(message)
        else:
            return "FAILED: You don't have the permissions"
    if Owners.get_owner(username, message.from_username) is not False:
        output = Messages.send_message_from_shop(message)
    else:
        return "FAILED: You are not authorized"
    if output:
        users = [message.to_username]
        if message.to_username == 'System':
            SMs = SystemManagers.get_all_system_managers()
            SM_names = []
            for sm in SMs:
                SM_names.append(sm.username)
            users = SM_names
        MessagingAlerts.notify_messaging_alerts(users,
                                                '<a href = "../app/home/messages/?content=received" >'
                                                ' You Have a new message from <strong>Shop</strong>' + message.from_username + '</a>')
        return "SUCCESS"
    else:
        return "FAILED"


def get_all_sent_messages(username):
    if username is not None:
        if get_user(username) is not False:
            return Messages.get_all_sent_messages(username)


def get_all_sent_shop_messages(username, shop_name):
    manager = StoreManagers.get_store_manager(username, shop_name)
    if manager is not False:
        if manager.permission_get_all_messages > 0:
            if Shops.search_shop(shop_name) is not False:
                return Messages.get_all_sent_shop_messages(shop_name)
    if Owners.get_owner(username, shop_name) is not False:
        if Shops.search_shop(shop_name) is not False:
            return Messages.get_all_sent_shop_messages(shop_name)
    return False


def get_received_system_messages():
    return Messages.get_received_system_messages()


def get_sent_system_messages():
    return Messages.get_sent_system_messages()
