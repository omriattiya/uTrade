from django.template import loader
from django.shortcuts import render
from DomainLayer import ShoppingLogic
from ServiceLayer import Consumer


def review_order(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        cart_count = 0
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
        else:
            cart_count = len(ShoppingLogic.get_guest_shopping_cart_item(guest))
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        if login is None:
            context = ShoppingLogic.order_of_guest(guest)
        else:
            context = ShoppingLogic.order_of_user(Consumer.loggedInUsers.get(login))
        context['topbar'] = topbar
        context['navbar'] = navbar
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
                cart_count = len(ShoppingLogic.get_cart_items(username))
                context = ShoppingLogic.order_of_user(Consumer.loggedInUsers.get(login))
            else:
                cart_count = len(ShoppingLogic.get_guest_shopping_cart_item(guest))
                context = ShoppingLogic.order_of_guest(guest)
        else:
            cart_count = len(ShoppingLogic.get_guest_shopping_cart_item(guest))
            context = ShoppingLogic.order_of_guest(guest)
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
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
