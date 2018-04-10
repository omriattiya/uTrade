from DatabaseLayer import RegisteredUsers, Owners

min_password_len = 6


def register(user):
    if user.username is not None and user.password is not None:
        if len(user.username) > 0 and (user.username[0] > '9' or user.username[0] < '0'):
            if len(user.password) >= min_password_len:
                return RegisteredUsers.addUser(user)
    else:
        return False


def edit_profile(user):
    if user.username is not None and user.password is not None:
        if len(user.password) > min_password_len:
            return RegisteredUsers.editUserPassword(user)
    return False


def login(user):
    if user.username is not None and user.password is not None:
        return RegisteredUsers.login(user)


#    _____
#   / ___ \
#  | |   | | _ _ _  ____    ____   ____   ___
#  | |   | || | | ||  _ \  / _  ) / ___) /___)
#  | |___| || | | || | | |( (/ / | |    |___ |
#   \_____/  \____||_| |_| \____)|_|    (___/
#

def add_owner(username, shop_id, target_user_id):
    if username is not None and \
            RegisteredUsers.get_user(username) is not False and \
            target_user_id is not None and shop_id is not None:
        return Owners.add_owner(shop_id, target_user_id)


def add_manager(username, shop_id, target_user_id):
    if username is not None and \
            RegisteredUsers.get_user(username) is not False and \
            target_user_id is not None and shop_id is not None:
        return Owners.add_manager(shop_id, target_user_id)

