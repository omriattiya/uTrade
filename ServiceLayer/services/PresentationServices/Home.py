from django.shortcuts import render
from django.template import loader

from DomainLayer import ShoppingLogic
from ServiceLayer.services.LiveAlerts import Consumer


def get_home(request):
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
        return render(request, 'index.html', context={'topbar': topbar, 'navbar': navbar})


def get_register(request):
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
        return render(request, 'register.html', context={'topbar': topbar, 'navbar': navbar})
