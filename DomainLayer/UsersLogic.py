from DatabaseLayer import RegisteredUsers, Owners, StoreManagers, Shops, SystemManagers

min_password_len = 6


def register(user):
    if user.username is not None and user.password is not None:
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

def add_owner(username, shop_name, target_username):
    if username is not None and \
                    RegisteredUsers.get_user(username) is not False and \
                    RegisteredUsers.get_user(target_username) is not False and shop_name is not None:
        return Owners.add_owner(shop_name, target_username)


def add_manager(username, shop_name, target_username, permissions):
    if username is not None and \
                    RegisteredUsers.get_user(username) is not False and \
                    RegisteredUsers.get_user(target_username) is not False and shop_name is not None:
        return StoreManagers.add_manager(shop_name, target_username, permissions)
    else:
        return False


def close_shop(username, shop_name):
    owner_of_shop = Owners.get_owner(username,shop_name)
    if owner_of_shop is not False:
        return Shops.close_shop(shop_name)
    else:
        return False


def re_open_shop(username, shop_name):
    owner_of_shop = Owners.get_owner(username,shop_name)
    if owner_of_shop is not False:
        return Shops.re_open_shop(shop_name)
    else:
        return False


def modify_notifications(owner_username, should_notify):
    return Owners.modify_notifications(owner_username, should_notify)
