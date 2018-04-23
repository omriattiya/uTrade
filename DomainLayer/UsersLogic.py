import re
import hashlib

from DatabaseLayer import RegisteredUsers, Owners, StoreManagers, Shops, SystemManagers, Discount

min_password_len = 6


def register(user):
    if user.username is not None and user.password is not None and not SystemManagers.is_system_manager(user.username):
        if re.match(r'[A-Za-z0-9]{8,20}', user.username):
            if re.match(r'[A-Za-z0-9]{8,20}', user.password):
                user.password = hashlib.sha256(user.password.encode()).hexdigest()
                return RegisteredUsers.add_user(user)
            else:
                return False
        else:
            return False
    else:
        return False


def edit_profile(user):
    status = RegisteredUsers.get_user(user.username)
    if status and user.username is not None and user.password is not None:
        if re.match(r'[A-Za-z0-9]{8,20}', user.password):
            user.password = hashlib.sha256(user.password.encode()).hexdigest()
            return RegisteredUsers.edit_user_password(user)
    return False


def login(user):
    if user.username is not None and user.password is not None:
        user.password = hashlib.sha256(user.password.encode()).hexdigest()
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
    return False


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


def add_visible_discount(disc, username):
    if disc is not None and username is not None:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_store = Owners.get_owner(username, disc.shop_name)
        if is_owner is not False or is_store is not False:
            return Discount.add_visible_discount(disc)
    return False


def add_invisible_discount(disc, username):
    if disc is not None and username is not None:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_store = Owners.get_owner(username, disc.shop_name)
        if is_owner is not False or is_store is not False:
            return Discount.add_invisible_discount(disc)
    return False


def get_visible_discount(item_id, shop_name):
    if item_id is not None and shop_name is not None:
        return Discount.get_visible_discount(item_id, shop_name)
    return False


def get_invisible_discount(item_id, shop_name, text):
    if item_id is not None and shop_name is not None and text is not None:
        return Discount.get_invisible_discount(item_id, shop_name, text)
    return False
