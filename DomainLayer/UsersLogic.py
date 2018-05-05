import hashlib
import re

from DatabaseLayer import RegisteredUsers, Owners, StoreManagers, Shops, SystemManagers, Discount

min_password_len = 6


def register(user):
    if user.username is not None and user.password is not None and not SystemManagers.is_system_manager(user.username):
        if re.match(r'[A-Za-z0-9]{8,20}', user.username):
            if re.match(r'[A-Za-z0-9]{8,20}', user.password):
                user.password = hashlib.sha256(user.password.encode()).hexdigest()
                if Shops.search_shop(user.username) is not False:
                    return False
                if RegisteredUsers.get_user(user.username) is not False:
                    return False
                return RegisteredUsers.add_user(user)
            else:
                return False
        else:
            return False
    else:
        return False


def get_registered_user(username):
    return RegisteredUsers.get_user(username)


def edit_password(user):
    if user.username == 'System':
        return False
    status = RegisteredUsers.get_user(user.username)
    if status and user.username is not None and user.password is not None:
        if re.match(r'[A-Za-z0-9]{8,20}', user.password):
            user.password = hashlib.sha256(user.password.encode()).hexdigest()
            return RegisteredUsers.edit_user_password(user)
    return False


def login(user):
    if SystemManagers.login(user.username, user.password):
        return True
    if user.username is not None and user.password is not None:
        user.password = hashlib.sha256(user.password.encode()).hexdigest()
        return RegisteredUsers.login(user)


# @username wants to remove the user @registered_user and if he is the last owner - delete the shop as well !
def remove_user(username, registered_user):
    if username is not None and registered_user is not None:
        if SystemManagers.is_system_manager(username) is not False:
            sys_manager = SystemManagers.is_system_manager(registered_user.username)
            is_store_manager = StoreManagers.is_store_manager(registered_user.username)
            is_owner = Owners.is_owner(registered_user.username)
            if sys_manager is False:
                user = RegisteredUsers.get_user(registered_user.username)
                if user is not False:
                    result_delete = True
                    if is_store_manager is not False:
                        result_delete = StoreManagers.remove_manager(registered_user.username)
                    else:
                        if is_owner is not False:
                            result_delete = Owners.remove_owner(registered_user.username)
                    return result_delete and RegisteredUsers.remove_user(registered_user.username)
            return False
    return False


def get_purchase_history(username):
    if username is not None:
        return RegisteredUsers.get_purchase_history(username)


# _____
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
                    RegisteredUsers.get_user(
                        store_manager.username) is not False and store_manager.store_name is not None:
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
    if system_manager.username == 'System':
        return False
    if RegisteredUsers.get_user(system_manager.username) is False and Shops.search_shop(
            system_manager.username) is False:
        return SystemManagers.add_system_manager(system_manager)


def add_visible_discount(disc, username):
    if disc is not None and username is not None and disc >= 0:
        is_owner = Owners.get_owner(username, disc.shop_name)
        is_store = Owners.get_owner(username, disc.shop_name)
        if is_owner is not False or is_store is not False:
            return Discount.add_visible_discount(disc)
    return False


def add_invisible_discount(disc, username):
    if disc is not None and username is not None and disc >= 0:
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


def get_owned_shops(username):
    return Owners.get_shops_by_owner(username)


def is_owner_of_shop(username, shop_name):
    results = get_owned_shops(username)
    for owner in results:
        if owner.shop_name == shop_name:
            return True
    return False

def get_managed_shops(username):
    return StoreManagers.get_manager_shops(username)


def is_owner_on_shop(username, shop_name):
    return Owners.is_owner_on_shop(username, shop_name)


def remove_store_manager(username, shop_name, target_id):
    if Owners.is_owner_on_shop(username, shop_name) is not False:
        return StoreManagers.remove_manager_from_shop(target_id, shop_name)
    return False


def update_permissions(username, store_manager):
    if Owners.is_owner_on_shop(username, store_manager.store_name) is not False:
        return StoreManagers.update_permissions(store_manager)
    return False


def is_system_manager(username):
    return SystemManagers.is_system_manager(username)


def get_all_users():
    return RegisteredUsers.get_all_users()


def is_manager_of_shop(username, shop_name):
    return StoreManagers.is_store_manager_of_shop(username, shop_name)


def get_manager(username, shop_name):
    return StoreManagers.get_store_manager(username, shop_name)
