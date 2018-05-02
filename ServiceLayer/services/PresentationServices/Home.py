from django.shortcuts import render
from django.template import loader

from ServiceLayer import Consumer


def get_home(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        # html of a regular user
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})

        return render(request, 'index.html', context={'topbar': topbar})


def get_register(request):
    if request.method == 'GET':
        return render(request, 'register.html', context=None)
