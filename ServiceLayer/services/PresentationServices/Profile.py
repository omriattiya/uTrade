from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import UsersLogic
from ServiceLayer import Consumer


def get_account(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                return render(request, 'customer-account.html', context={'topbar': topbar})

        return HttpResponse('You are not logged in!')


def get_shops(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                owned_shops_html = ""
                owned_shops = UsersLogic.get_owned_shops(username)
                for owned_shop in owned_shops:
                    owned_shops_html += loader.render_to_string('components/ShopYouOwn.html', context={
                        'shop_name': owned_shop.shop_name,
                        'review': "NSY",
                        'status': "NSY",
                        'notify': owned_shop.should_notify,
                    })

                return render(request, 'customer-shops.html', context={'topbar': topbar, 'owned_shops': owned_shops_html})

        return HttpResponse('You are not logged in!')
