from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import ShopLogic, UsersLogic, ItemsLogic
from DomainLayer import ShoppingLogic
from ServiceLayer import Consumer
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.ShopReview import ShopReview

shop_not_exist = 'shop does not exist'
not_get_request = 'not a get request'
error_login_owner = 'must be logged in as owner'


def add_to_db():
    shop_name = 'my_shop'
    username = 'omriatti'
    UsersLogic.register(RegisteredUser(username, '12345678'))
    ShopLogic.create_shop(Shop(shop_name, 'Active'), username)
    ItemsLogic.add_item_to_shop(Item(1, shop_name, 'tomato-2', 'fruits', '', 20, 70, 'regular',
                                     'https://nutriliving-images.imgix.net/images/2014/266/1440/5B26E568-4243-E411-B834-22000AF88B16.jpg?ch=DPR&w=500&h=500&auto=compress,format&dpr=1&ixlib=imgixjs-3.0.4'),
                                username)
    ShopLogic.add_review_on_shop(ShopReview(username, "THIS IS AMAZING SHOP I BUT HERE EVERY DAY", 5, shop_name))


def get_shop(request):
    add_to_db()
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
            every_html = {'top_bar': top_bar, 'nav_bar': nav_bar}

            items = ShopLogic.get_shop_items(shop.name)
            products = ""
            for item in items:
                products += loader.render_to_string('component/item.html',
                                                    {'every_html': every_html, 'name': item.name, 'price': item.price,
                                                     'url': item.url, 'item_id': item.id}, None,
                                                    None)
            owner_manager_options = ""
            render_edit_remove = loader.render_to_string('component/owner_manager_options.html',
                                                         {'path': 'owner/items',
                                                          'shop_name': shop_name,
                                                          'button_text': 'Edit & Remove Items'})
            render_purchase_history = loader.render_to_string('component/owner_manager_options.html',
                                                              {'path': 'owner/purchase_history',
                                                               'shop_name': shop_name,
                                                               'button_text': 'Purchase History'})

            if UsersLogic.is_owner_of_shop(username, shop_name):
                owner_manager_options += render_purchase_history + render_edit_remove
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.permission_get_purchased_history == 1:
                    owner_manager_options += render_purchase_history
                if manager.permission_edit_item == 1 or manager.permission_remove_item == 1:
                    owner_manager_options += render_edit_remove

            context = {'shop_name': shop.name,
                       'shop_status': shop.status,
                       'products': products,
                       'owner_manager_options': owner_manager_options}
            return render(request, 'shop.html', context=context)
        else:
            return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_reviews(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            reviews = ShopLogic.get_shop_reviews(shop_name)
            string_reviews = ""
            for review in reviews:
                string_reviews += loader.render_to_string('component/review.html',
                                                          {'writer_name': review.writerId,
                                                           'rank': review.rank,
                                                           'description': review.description}, None, None)
            context = {'shop_name': shop_name, 'reviews': string_reviews}
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
                string_items += loader.render_to_string('component/item_owner.html',
                                                        {'item_name': item.name,
                                                         'item_quantity': item.quantity,
                                                         'item_category': item.category,
                                                         'item_keywords': item.keyWords,
                                                         'item_price': item.price,
                                                         'item_url': item.url,
                                                         'item_id': item.id})
            return render(request, 'shop_view_for_owner.html',
                          context={'every_html': every_html, 'items': string_items})
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
        if UsersLogic.is_owner_of_shop(username, shop_name) is not False:
            shop_items = ShopLogic.get_shop_purchase_history(username, shop_name)
            string_items = ""
            for item in shop_items:
                string_items += loader.render_to_string('component/purchase_item_owner.html',
                                                        {'purchase_id': item.purchase_id,
                                                         'item_id': item.item_id,
                                                         'quantity': item.quantity,
                                                         'price': item.price})
            return render(request, 'shop_view_purchase_history.html',
                          context={'every_html': every_html, 'items': string_items})
        return HttpResponse(shop_not_exist + " with username=" + username)
    return HttpResponse(not_get_request)
