from django.template import loader

from DomainLayer import UserShoppingCartLogic, GuestShoppingCartLogic
from ServiceLayer.services.LiveAlerts import Consumer


def get_top_bar(login):
    topbar = loader.render_to_string('components/Topbar.html', context=None)
    if login is not None:
        username = Consumer.loggedInUsers.get(login)
        if username is not None:
            topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
    return topbar


def get_nav_bar(login, guest):
    cart_count = 0
    if login is not None:
        username = Consumer.loggedInUsers.get(login)
        if username is not None:
            cart_count = len(UserShoppingCartLogic.get_cart_items(login))
        else:
            if guest is not None:
                cart_count = len(GuestShoppingCartLogic.get_guest_shopping_cart_item(guest))
    else:
        if guest is not None:
            cart_count = len(GuestShoppingCartLogic.get_guest_shopping_cart_item(guest))
    return loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
