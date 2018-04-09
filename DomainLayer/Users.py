from DatabaseLayer import Users


def remove_user(username):
    if username is not None:
        return Users.remove_user(username)
