from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import ShopLogic, UsersLogic
from DomainLayer import ShoppingLogic
from ServiceLayer.services.LiveAlerts import Consumer

shop_not_exist = 'shop does not exist'
not_get_request = 'not a get request'
error_login_owner = 'must be logged in as owner'
error_login = 'must be logged in'


def get_shop(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            login = request.COOKIES.get('login_hash')
            cart_count = 0
            top_bar = loader.render_to_string('components/Topbar.html', context=None)
            username = None
            if login is not None:
                username = Consumer.loggedInUsers.get(login)
                if username is not None:
                    # html of a logged in user
                    top_bar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                    cart_count = len(ShoppingLogic.get_cart_items(username))
            nav_bar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})

            items = ShopLogic.get_shop_items(shop.name)
            products = ""
            for item in items:
                products += loader.render_to_string(
                    'component/../../../PresentationLayer/templates/components/item.html',
                    {'name': item.name, 'price': item.price,
                                                     'url': item.url, 'item_id': item.id}, None,
                    None)
            owner_manager_options = ""
            render_edit_remove = loader.render_to_string(
                'component/../../../PresentationLayer/templates/components/owner_manager_options.html',
                {'path': 'owner/items',
                                                          'shop_name': shop_name,
                                                          'button_text': 'Edit & Remove Items'})
            render_purchase_history = loader.render_to_string(
                'component/../../../PresentationLayer/templates/components/owner_manager_options.html',
                {'path': 'owner/purchase_history',
                                                               'shop_name': shop_name,
                                                               'button_text': 'Purchase History'})
            render_add_item = loader.render_to_string(
                'component/../../../PresentationLayer/templates/components/owner_manager_options.html',
                {'path': 'owner/items/add_item',
                                                       'shop_name': shop_name,
                                                       'button_text': 'Add Item'})

            if UsersLogic.is_owner_of_shop(username, shop_name):
                owner_manager_options += render_purchase_history + render_edit_remove + render_add_item
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.permission_get_purchased_history == 1:
                    owner_manager_options += render_purchase_history
                if manager.permission_edit_item == 1 or manager.permission_remove_item == 1:
                    owner_manager_options += render_edit_remove
                if manager.permission_add_item == 1:
                    owner_manager_options += render_add_item

            context = {'shop_name': shop.name,
                       'shop_status': shop.status,
                       'products': products,
                       'owner_manager_options': owner_manager_options,
                       'topbar': top_bar, 'navbar': nav_bar, }
            return render(request, 'shop.html', context=context)
        else:
            return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_reviews(request):
    if request.method == 'GET':

        login = request.COOKIES.get('login_hash')
        cart_count = 0
        top_bar = loader.render_to_string('components/Topbar.html', context=None)
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                top_bar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))

        nav_bar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})

        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            reviews = ShopLogic.get_shop_reviews(shop_name)
            string_reviews = ""
            for review in reviews:
                string_reviews += loader.render_to_string(
                    'component/../../../PresentationLayer/templates/components/review.html',
                    {'writer_name': review.writerId,
                                                           'rank': review.rank,
                                                           'description': review.description}, None, None)
            context = {'topbar': top_bar, 'navbar': nav_bar, 'shop_name': shop_name, 'reviews': string_reviews}
            return render(request, 'shop_reviews.html', context=context)
        return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_shop_to_owner(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')

        login = request.COOKIES.get('login_hash')
        cart_count = 0
        top_bar = loader.render_to_string('components/Topbar.html', context=None)
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                top_bar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
            else:
                return HttpResponse(error_login_owner)
        else:
            return HttpResponse(error_login_owner)

        nav_bar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        every_html = {'top_bar': top_bar, 'nav_bar': nav_bar}
        if UsersLogic.is_owner_of_shop(username, shop_name) is not False:
            shop_items = ShopLogic.get_shop_items(shop_name)
            string_items = ""
            for item in shop_items:
                string_items += loader.render_to_string(
                    'component/../../../PresentationLayer/templates/components/item_owner.html',
                    {'item_name': item.name,
                                                         'item_quantity': item.quantity,
                                                         'item_category': item.category,
                                                         'item_keywords': item.keyWords,
                                                         'item_price': item.price,
                                                         'item_url': item.url,
                                                         'item_id': item.id,
                                                         'shop_name': item.shop_name})
            return render(request, 'shop_view_for_owner.html',
                          context={'topbar': top_bar, 'navbar': nav_bar, 'items': string_items, 'shop_name': shop_name})
        return HttpResponse(shop_not_exist + " with username=" + username)
    return HttpResponse(not_get_request)


def get_shop_managers(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_system_manager(username):
                    shops = ShopLogic.get_store_managers(shop_name)
                    shops_string = ""
                    for shop in shops:
                        shops_string += shop.username + "\n"
                    return HttpResponse(shops_string)
        return HttpResponse('fail')


def get_shop_owner(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_system_manager(username):
                    shops = ShopLogic.get_store_owners(shop_name)
                    shops_string = ""
                    for shop in shops:
                        shops_string += shop.username + "\n"
                    return HttpResponse(shops_string)
        return HttpResponse('fail')


def watch_purchase_history(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')

        login = request.COOKIES.get('login_hash')
        cart_count = 0
        top_bar = loader.render_to_string('components/Topbar.html', context=None)
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                top_bar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
            else:
                return HttpResponse(error_login_owner)
        else:
            return HttpResponse(error_login_owner)

        if not UsersLogic.is_owner_of_shop(username, shop_name):
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.permission_get_purchased_history is not 1:  # no permission
                    return HttpResponse('no permission to watch purchase history')
            else:
                return HttpResponse('fail')  # not manager not owner

        nav_bar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        every_html = {'top_bar': top_bar, 'nav_bar': nav_bar}
        shop_items = ShopLogic.get_shop_purchase_history(username, shop_name)
        string_items = ""
        for item in shop_items:
            string_items += loader.render_to_string(
                'component/../../../PresentationLayer/templates/components/purchase_item_owner.html',
                {'purchase_id': item.purchase_id,
                                                     'item_id': item.item_id,
                                                     'quantity': item.quantity,
                                                     'price': item.price})
        return render(request, 'shop_view_purchase_history.html',
                      context={'every_html': every_html, 'items': string_items, 'shop_name': shop_name})
    return HttpResponse(not_get_request)


def add_item_to_shop(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')

        login = request.COOKIES.get('login_hash')
        cart_count = 0
        top_bar = loader.render_to_string('components/Topbar.html', context=None)
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                top_bar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
            else:
                return HttpResponse(error_login_owner)
        else:
            return HttpResponse(error_login_owner)

        if not UsersLogic.is_owner_of_shop(username, shop_name):
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.permission_add_item is not 1:  # no permission
                    return HttpResponse('no permission to add item')
            else:
                return HttpResponse('fail')  # not manager not owner

        nav_bar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        every_html = {'top_bar': top_bar, 'nav_bar': nav_bar}
        return render(request, 'shop_add_item.html',
                      context={'every_html': every_html, 'shop_name': shop_name})


def add_review(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')

        login = request.COOKIES.get('login_hash')
        cart_count = 0
        top_bar = loader.render_to_string('components/Topbar.html', context=None)
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                top_bar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
            else:
                return HttpResponse(error_login)
        else:
            return HttpResponse(error_login)

        nav_bar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})

        return render(request, 'add_review.html',
                      context={'topbar': top_bar, 'navbar': nav_bar, 'shop_name': shop_name})
