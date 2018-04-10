from DatabaseLayer import Users


def remove_user(username, registered_user):
    if username is not None and registered_user is not None:
        # if check_logged_in(username)
        return Users.remove_user(registered_user)
