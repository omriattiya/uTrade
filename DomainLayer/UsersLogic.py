from struct import pack

from DatabaseLayer import RegisteredUsers, Owners, StoreManagers, Shops, SystemManagers

min_password_len = 6


def register(user):
    if user.username is not None and user.password is not None and not SystemManagers.is_system_manager(user.username):
        if len(user.username) > 0 and (user.username[0] > '9' or user.username[0] < '0'):
            if len(user.password) >= min_password_len:
                return RegisteredUsers.add_user(user)
    else:
        return False


def edit_profile(user):
    if user.username is not None and user.password is not None:
        if len(user.password) > min_password_len:
            return RegisteredUsers.edit_user_password(user)
    return False


def login(user):
    if user.username is not None and user.password is not None:
        return RegisteredUsers.login(user)


def remove_user(username, registered_user):
    if username is not None and registered_user is not None:
        sys_manager = SystemManagers.is_system_manager(username)
        if sys_manager is not False:
            user = RegisteredUsers.get_user(registered_user)
            if user is not False:
                return RegisteredUsers.remove_user(registered_user)
        return False
    return False


def get_purchase_history(username):
    if username is not None:
        return RegisteredUsers.get_purchase_history(username)


#    _____
#   / ___ \
#  | |   | | _ _ _  ____    ____   ____   ___
#  | |   | || | | ||  _ \  / _  ) / ___) /___)
#  | |___| || | | || | | |( (/ / | |    |___ |
#   \_____/  \____||_| |_| \____)|_|    (___/
#

def add_owner(username, owner):
    if username is not None and \
            Owners.get_owner(username, owner.shop_name) is not False and \
            RegisteredUsers.get_user(owner.username) is not False and owner.shop_name is not None:
        return Owners.add_owner(owner)


def add_manager(username, store_manager):
    if username is not None and \
            Owners.get_owner(username, store_manager.store_name) is not False and \
            RegisteredUsers.get_user(store_manager.username) is not False and store_manager.store_name is not None:
        return StoreManagers.add_manager(store_manager)
    else:
        return False


def close_shop(username, shop_name):
    owner_of_shop = Owners.get_owner(username, shop_name)
    if owner_of_shop is not False:
        return Shops.close_shop(shop_name)
    else:
        return False


def re_open_shop(username, shop_name):
    owner_of_shop = Owners.get_owner(username, shop_name)
    if owner_of_shop is not False:
        return Shops.re_open_shop(shop_name)
    else:
        return False


def modify_notifications(owner_username, should_notify):
    return Owners.modify_notifications(owner_username, should_notify)


def add_system_manager(system_manager):
    if RegisteredUsers.get_user(system_manager.username) is False:
        return SystemManagers.add_system_manager(system_manager)
    else:
        return False
