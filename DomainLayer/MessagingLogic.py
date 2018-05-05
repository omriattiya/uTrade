from django.http import HttpResponse

from DatabaseLayer import Messages, StoreManagers, Owners, Shops, SystemManagers
from DomainLayer import UsersLogic
from ServiceLayer import Consumer
from SharedClasses import Message
from DatabaseLayer.RegisteredUsers import get_user


def send_message(message):
    output = False
    if message.from_username is not None and message.to_username is not None and message.content is not None:
        if get_user(message.from_username) is not False:
            if get_user(message.to_username) is not False:
                output = Messages.send_message(message)
            elif message.to_username == 'System':
                output = Messages.send_message(message)
        if SystemManagers.is_system_manager(message.from_username):
            message.from_username = 'System'
            output = Messages.send_message(message)
    if output:
        users = [message.to_username]
        if message.to_username == 'System':
            SMs = SystemManagers.get_all_system_managers()
            SM_names = []
            for sm in SMs:
                SM_names.append(sm.username)
            users = SM_names
        Consumer.notify_live_alerts(users,
                                    '<a href = "http://localhost:8000/app/home/messages/?content=received" > '
                                    'You Have a new message from ' + message.from_username + '</a>')
    return output


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
    if manager is not False:
        if manager.permission_reply_messages > 0:
            if Shops.search_shop(message.from_username) is not False:
                output = Messages.send_message_from_shop(message)
    if Owners.get_owner(username, message.from_username) is not False:
        if Shops.search_shop(message.from_username) is not False:
            output = Messages.send_message_from_shop(message)
    if output:
        users = [message.to_username]
        if message.to_username == 'System':
            SMs = SystemManagers.get_all_system_managers()
            SM_names = []
            for sm in SMs:
                SM_names.append(sm.username)
            users = SM_names
        Consumer.notify_live_alerts(users,
                                    '<a href = "http://localhost:8000/app/home/messages/?content=received" >'
                                    ' You Have a new message from <strong>Shop</strong>' + message.from_username + '</a>')
    return output


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
