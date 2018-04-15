from DomainLayer import UsersLogic
from SharedClasses.RegisteredUser import RegisteredUser


def register_user(username, password):
    return UsersLogic.RegisteredUsers.add_user(RegisteredUser(username, password))


def login(username, password):
    UsersLogic.login(RegisteredUser(username, password))
