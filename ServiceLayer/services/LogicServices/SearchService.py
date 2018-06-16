from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import SearchLogic, LoggerLogic
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar


def search_item(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest')
        topbar = Topbar_Navbar.get_top_bar(login)
        navbar = Topbar_Navbar.get_nav_bar(login, guest)
        search_by = request.GET.get('searchBy')
        items = []
        words = []

        event = "SEARCH ITEM"

        if search_by == 'name':
            name = request.GET.get('name')

            suspect_sql_injection = LoggerLogic.identify_sql_injection(name, event)
            if suspect_sql_injection:
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            items = SearchLogic.search_by_name(name)
            if len(items) != 0:
                context = {'topbar': topbar, 'items': items, 'navbar': navbar, 'len': len(items)}
                return render(request, 'SearchView.html', context)
            else:
                words = SearchLogic.get_similar_words(name)
                words = words[:5]
                items_names_that_exists = []
                for each_item in words:
                    item = SearchLogic.search_by_name(each_item)
                    if len(item) != 0:
                        items_names_that_exists.append(each_item)
                context = {'topbar': topbar, 'items': items_names_that_exists, 'navbar': navbar, 'type': 'name'}
                if len(items_names_that_exists) != 0:
                    return render(request, 'ItemsNotFound.html', context)
                else:
                    return render(request, 'ItemNotFoundNoSuggestions.html', context)
        if search_by == 'category':
            category = request.GET.get('category')

            suspect_sql_injection = LoggerLogic.identify_sql_injection(category, event)
            if suspect_sql_injection:
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            items = SearchLogic.search_by_category(category)
            if len(items) != 0:
                context = {'topbar': topbar, 'items': items, 'navbar': navbar, 'len': len(items)}
                return render(request, 'SearchView.html', context)
            else:
                words = SearchLogic.get_similar_words(category)
                words = words[:5]
                items_names_that_exists = []
                for each_item in words:
                    item = SearchLogic.search_by_category(each_item)
                    if len(item) != 0:
                        items_names_that_exists.append(each_item)
                context = {'topbar': topbar, 'items': items_names_that_exists, 'navbar': navbar, 'type': 'category'}
                if len(items_names_that_exists) != 0:
                    return render(request, 'ItemsNotFound.html', context)
                else:
                    return render(request, 'ItemNotFoundNoSuggestions.html', context)
        if search_by == 'keywords':
            keywords = request.GET.get('keywords')

            suspect_sql_injection = LoggerLogic.identify_sql_injection(keywords, event)
            if suspect_sql_injection:
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            items = SearchLogic.search_by_keywords(keywords)
            if len(items) != 0:
                context = {'topbar': topbar, 'items': items, 'navbar': navbar, 'len': len(items)}
                return render(request, 'SearchView.html', context)
            else:
                words = SearchLogic.get_similar_words(keywords)
                words = words[:5]
                items_names_that_exists = []
                for each_item in words:
                    item = SearchLogic.search_by_keywords(each_item)
                    if len(item) != 0:
                        items_names_that_exists.append(each_item)
                context = {'topbar': topbar, 'items': items_names_that_exists, 'navbar': navbar, 'type': 'keywords'}
                if len(items_names_that_exists) != 0:
                    return render(request, 'ItemsNotFound.html', context)
                else:
                    return render(request, 'ItemNotFoundNoSuggestions.html', context)


def search_shop(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        words = []
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
        name = request.GET.get('name')

        suspect_sql_injection = LoggerLogic.identify_sql_injection(name, "SEARCH SHOP")
        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        shop = SearchLogic.search_shop(name)
        if shop is not False:
            context = {'topbar': topbar}
            return render(request, 'shop.html', context)
        else:
            words = SearchLogic.get_similar_words(name)
            words = words[:5]
            context = {'topbar': topbar, 'words': words}
            return render(request, 'ItemsNotFound.html', context)


def search_item_in_shop(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})

        name = request.GET.get('item_name')
        shop_name = request.GET.get('shop_name')

        event = "SEARCH ITEM IN SHOP"
        suspect_sql_injection = False
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(name, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(shop_name, event)

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        item = SearchLogic.search_item_in_shop(name, shop_name)
        if item is not False:
            context = {'topbar': topbar, 'item': item}
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

        shop_name = request.GET.get('shop_name')

        event = "SEARCH ITEMS IN SHOP"
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event)

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        items = SearchLogic.search_items_in_shop(shop_name)
        if items is not False:
            context = {'topbar': topbar, 'items': items}
            return render(request, 'SearchView.html', context)
