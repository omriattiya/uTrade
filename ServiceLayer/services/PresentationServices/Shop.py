from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import ShopLogic, UsersLogic, ShoppingLogic, DiscountLogic
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar

shop_not_exist = 'shop does not exist'
not_get_request = 'not a get request'
error_login_owner = 'must be logged in as owner'
error_login = 'must be logged in'


# TODO: get_visible_category_discount
def percent_of_discount(id, category, shop_name):
    item_discount = DiscountLogic.get_visible_discount(id, shop_name)
    if item_discount is not False:
        return 1.0 - item_discount.percentage / 100
    category_discount = DiscountLogic.get_visible_discount_category(category, shop_name)
    if category_discount is not False:
        return 1.0 - category_discount.percentage / 100
    return 1


def get_shop(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            username = None
            login = request.COOKIES.get('login_hash')
            if login is not None:
                username = Consumer.loggedInUsers.get(login)
            guest = request.COOKIES.get('guest_hash')
            context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
            items = ShopLogic.get_shop_items(shop.name)
            products = ""
            for item in items:
                if item.kind == 'prize':
                    continue
                products += loader.render_to_string(
                    'components/item.html',
                    {'name': item.name, 'price': item.price * percent_of_discount(item.id, item.category, shop_name),
                     'url': item.url, 'item_id': item.id}, None,
                    None)
            owner_manager_options = ""
            render_edit_remove = loader.render_to_string(
                'components/owner_manager_options.html',
                {'path': 'owner/items',
                 'shop_name': shop_name,
                 'button_text': 'Edit & Remove Items'})
            render_purchase_history = loader.render_to_string(
                'components/owner_manager_options.html',
                {'path': 'owner/purchase_history',
                 'shop_name': shop_name,
                 'button_text': 'Purchase History'})
            render_add_item = loader.render_to_string(
                'components/owner_manager_options.html',
                {'path': 'owner/items/add_item',
                 'shop_name': shop_name,
                 'button_text': 'Add Item'})
            render_add_discount = loader.render_to_string(
                'components/owner_manager_options.html',
                {'path': 'owner/add_discount',
                 'shop_name': shop_name,
                 'button_text': 'Add Discount'})
            render_delete_discount = loader.render_to_string(
                'components/owner_manager_options.html',
                {'path': 'owner/delete_discount',
                 'shop_name': shop_name,
                 'button_text': 'Delete Discount'})

            if UsersLogic.is_owner_of_shop(username, shop_name):
                owner_manager_options += render_purchase_history + \
                                         render_edit_remove + \
                                         render_add_item + \
                                         render_add_discount + \
                                         render_delete_discount
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.permission_get_purchased_history == 1:
                    owner_manager_options += render_purchase_history
                if manager.permission_edit_item == 1 or manager.permission_remove_item == 1:
                    owner_manager_options += render_edit_remove
                if manager.permission_add_item == 1:
                    owner_manager_options += render_add_item
                if manager.discount_permission == 1:
                    owner_manager_options += render_add_discount + render_delete_discount

            context.update({'shop_name': shop.name,
                            'shop_status': shop.status,
                            'products': products,
                            'owner_manager_options': owner_manager_options})
            return render(request, 'shop.html', context=context)
        else:
            login = request.COOKIES.get('login_hash')
            guest = request.COOKIES.get('guest')
            topbar = Topbar_Navbar.get_top_bar(login)
            navbar = Topbar_Navbar.get_nav_bar(login, guest)
            context = {'topbar': topbar, 'navbar': navbar}
            return render(request, 'ShopNotFound.html', context)
    return HttpResponse(not_get_request)


def get_reviews(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            reviews = ShopLogic.get_shop_reviews(shop_name)
            string_reviews = ""
            for review in reviews:
                string_reviews += loader.render_to_string(
                    'components/review.html',
                    {'writer_name': review.writerId,
                     'rank': review.rank,
                     'description': review.description}, None, None)
            context.update({'shop_name': shop_name, 'reviews': string_reviews})
            return render(request, 'shop_reviews.html', context=context)
        return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_shop_to_owner(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse(error_login_owner)
        else:
            return HttpResponse(error_login_owner)
        if UsersLogic.is_owner_of_shop(username, shop_name) is not False:
            shop_items = ShopLogic.get_shop_items(shop_name)
            string_items = ""
            for item in shop_items:
                string_items += loader.render_to_string(
                    'components/item_owner.html',
                    {'item_name': item.name,
                     'item_quantity': item.quantity,
                     'item_category': item.category,
                     'item_keywords': item.keyWords,
                     'item_price': item.price,
                     'item_url': item.url,
                     'item_id': item.id,
                     'shop_name': item.shop_name})
            context.update({'items': string_items, 'shop_name': shop_name})
            return render(request, 'shop_items_management.html',
                          context=context)
        else:
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
        guest = request.COOKIES.get('guest_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
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

        every_html = {'top_bar': Topbar_Navbar.get_top_bar(login), 'nav_bar': Topbar_Navbar.get_nav_bar(login, guest)}
        shop_items = ShopLogic.get_shop_purchase_history(username, shop_name)
        string_items = ""
        for item in shop_items:
            string_items += loader.render_to_string(
                'components/purchase_item_owner.html',
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
        guest = request.COOKIES.get('guest_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
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
        every_html = {'top_bar': Topbar_Navbar.get_top_bar(login), 'nav_bar': Topbar_Navbar.get_nav_bar(login, guest)}
        return render(request, 'shop_add_item.html',
                      context={'every_html': every_html, 'shop_name': shop_name})


def add_discount_page(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse(error_login_owner)
        else:
            return HttpResponse(error_login_owner)
        if not UsersLogic.is_owner_of_shop(username, shop_name):
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.discount_permission is not 1:  # no permission
                    return HttpResponse('no permission to add discount')
            else:
                return HttpResponse('fail')  # not manager not owner
        every_html = {'top_bar': Topbar_Navbar.get_top_bar(login), 'nav_bar': Topbar_Navbar.get_nav_bar(login, guest)}
        return render(request, 'shop_add_discount.html',
                      context={'every_html': every_html, 'shop_name': shop_name})


def delete_discount(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse(error_login_owner)
        else:
            return HttpResponse(error_login_owner)
        if not UsersLogic.is_owner_of_shop(username, shop_name):
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.discount_permission is not 1:  # no permission
                    return HttpResponse('no permission to add discount')
            else:
                return HttpResponse('fail')  # not manager not owner

        # TODO: get all visible discounts
        shop_discounts = ShoppingLogic.get_visible_discount(shop_name)
        string_discounts = ""
        for discount in shop_discounts:
            string_discounts += loader.render_to_string(
                'components/discount.html',
                {'shop_name': shop_name,
                 'item_id': discount.item_id,
                 'from_date': discount.from_date,
                 })

        every_html = {'top_bar': Topbar_Navbar.get_top_bar(login), 'nav_bar': Topbar_Navbar.get_nav_bar(login, guest)}
        return render(request, 'shop_delete_discount.html',
                      context={'every_html': every_html, 'shop_name': shop_name, 'discounts': string_discounts})
