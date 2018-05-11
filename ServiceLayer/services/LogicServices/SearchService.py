from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import SearchLogic, ShoppingLogic
from ServiceLayer.services.LiveAlerts import Consumer


def search_item(request):
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
        search_by = request.GET.get('searchBy')
        items = []
        if search_by == 'name':
            items = SearchLogic.search_by_name(request.GET.get('name'))
            if len(items) != 0:
                context = {'topbar': topbar, 'items': items, 'navbar': navbar}
                return render(request, 'SearchView.html', context)
            else:
                return HttpResponse('There Are Not Match Items.')
        if search_by == 'category':
            items = SearchLogic.search_by_category(request.GET.get('category'))
            if len(items) != 0:
                context = {'topbar': topbar, 'items': items, 'navbar': navbar}
                return render(request, 'SearchView.html', context)
            else:
                return HttpResponse('There Are Not Match Items.')
        if search_by == 'keywords':
            items = SearchLogic.search_by_keywords(request.GET.get('keywords'))
            if len(items) != 0:
                context = {'topbar': topbar, 'items': items, 'navbar': navbar}
                return render(request, 'SearchView.html', context)
            else:
                return HttpResponse('There Are Not Match Items.')


def search_shop(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
        shop = SearchLogic.search_shop(request.GET.get('name'))
        if shop is not False:
            context = {'topbar': topbar}
            return render(request, 'shop.html', context)
        else:
            return HttpResponse('There Is Not Shop With This Name.')


def search_item_in_shop(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
        item = SearchLogic.search_item_in_shop(request.GET.get('item_name'), request.GET.get('shop_name'))
        if item is not False:
            context = {'topbar': topbar ,'item': item}
            return render(request, 'SearchView.html', context)


def search_items_in_shop(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
        items = SearchLogic.search_items_in_shop(request.GET.get('item_name'), request.GET.get('shop_name'))
        if items is not False:
            context = {'topbar': topbar ,'items': items}
            return render(request, 'SearchView.html', context)
