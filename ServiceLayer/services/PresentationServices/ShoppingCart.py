from django.shortcuts import render
from DomainLayer import ShoppingLogic, UserShoppingCartLogic, GuestShoppingCartLogic
from ServiceLayer import Consumer
from django.template import loader

from DomainLayer import ShoppingLogic
from ServiceLayer.services.LiveAlerts import Consumer


def review_order(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        cart_count = 0
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(UserShoppingCartLogic.get_cart_items(login))
        else:
            cart_count = len(GuestShoppingCartLogic.get_guest_shopping_cart_item(guest))
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        if login is None:
            context = GuestShoppingCartLogic.order_of_guest(guest)
        else:
            context = UserShoppingCartLogic.order_of_user(login)
        context['topbar'] = topbar
        context['navbar'] = navbar
        username = Consumer.loggedInUsers.get(login)
        context['username'] = username
        return render(request, 'checkout4.html', context=context)


def get_cart_items(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        cart_count = 0
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        context = {}
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(UserShoppingCartLogic.get_cart_items(login))
                context = UserShoppingCartLogic.order_of_user(login)
            else:
                if guest is not None:
                    cart_count = len(GuestShoppingCartLogic.get_guest_shopping_cart_item(guest))
                    context = GuestShoppingCartLogic.order_of_guest(guest)
        else:
            if guest is not None:
                cart_count = len(GuestShoppingCartLogic.get_guest_shopping_cart_item(guest))
                context = GuestShoppingCartLogic.order_of_guest(guest)
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        if login is None:
            context = ShoppingLogic.order_helper(guest)
        else:
            context = ShoppingLogic.order_helper(Consumer.loggedInUsers.get(login))
        context['topbar'] = topbar
        context['navbar'] = navbar
        return render(request, 'basket.html', context=context)


def address(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        cart_count = 0
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        context = {'topbar': topbar, 'navbar': navbar}
        return render(request, 'checkout1.html', context=context)
