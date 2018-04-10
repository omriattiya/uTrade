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


def add_owner(user, shop_id, receiver_user_id):
    if user.username is not None and \
            RegisteredUsers.get_user(user.username) is not False and\
            receiver_user_id is not None and shop_id is not None:
        return Owners.add_owner(shop_id, receiver_user_id)