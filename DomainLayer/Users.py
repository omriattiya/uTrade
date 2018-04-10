from DatabaseLayer import RegisteredUsers

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
