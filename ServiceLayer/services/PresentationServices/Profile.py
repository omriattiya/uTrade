from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import UsersLogic, ShopLogic, ShoppingLogic, ItemsLogic
from ServiceLayer import Consumer


def get_account(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                system_hidden = "hidden"
                if UsersLogic.is_system_manager(username):
                    system_hidden = ""

                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
                navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
                return render(request, 'customer-account.html',
                              context={'topbar': topbar, 'navbar': navbar, 'system_hidden': system_hidden})

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
                    shop = ShopLogic.search_shop(owned_shop.shop_name)
                    rank = ShopLogic.get_shop_rank(shop.name)

                    if shop.status == 'Active':
                        status_class = 'btn btn-success btn-sm'
                    elif shop.status == 'Inactive':
                        status_class = 'btn btn-warning btn-sm'
                    else:
                        status_class = 'btn btn-danger btn-sm'
                    owned_shops_html += loader.render_to_string('components/ShopYouOwn.html', context={
                        'shop_name': owned_shop.shop_name,
                        'review': rank,
                        'status': shop.status,
                        'status_button_class': status_class,
                    })

                managed_shops_html = ""
                managed_shops = UsersLogic.get_managed_shops(username)
                yes_no_array = ['No', 'Yes']
                for managed_shop in managed_shops:
                    rank = ShopLogic.get_shop_rank(managed_shop.username)
                    _shop = ShopLogic.search_shop(managed_shop.store_name)
                    managed_shops_html += loader.render_to_string('components/ShopsYouManage.html', context={
                        'shop_name': _shop.name,
                        'review': rank,
                        'status': _shop.status,
                        'AIP': yes_no_array[managed_shop.permission_add_item],
                        'RIP': yes_no_array[managed_shop.permission_remove_item],
                        'EIP': yes_no_array[managed_shop.permission_edit_item],
                        'RMP': yes_no_array[managed_shop.permission_reply_messages],
                        'GAP': yes_no_array[managed_shop.permission_get_all_messages],
                        'GPHP': yes_no_array[managed_shop.permission_get_purchased_history],
                        'DP': yes_no_array[managed_shop.discount_permission],

                    })

                cart_count = len(ShoppingLogic.get_cart_items(username))
                navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
                return render(request, 'customer-shops.html', context={
                    'topbar': topbar,
                    'owned_shops': owned_shops_html,
                    'managed_shops': managed_shops_html,
                    'navbar': navbar})

        return HttpResponse('You are not logged in!')


def get_managers(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        shop_name = request.GET.get('shop_name')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_owner_on_shop(username, shop_name) is not False:
                    managers_html = ""
                    managers = ShopLogic.get_store_managers(shop_name)
                    for manager in managers:
                        check_array = ["", "checked"]
                        managers_html += loader.render_to_string('components/ManagersOnShop.html', context={
                            'manager_name': manager.username,
                            'checked_AIP': check_array[manager.permission_add_item],
                            'checked_RIP': check_array[manager.permission_remove_item],
                            'checked_EIP': check_array[manager.permission_edit_item],
                            'checked_RMP': check_array[manager.permission_reply_messages],
                            'checked_GAP': check_array[manager.permission_get_all_messages],
                            'checked_GPHP': check_array[manager.permission_get_purchased_history],
                            'checked_DP': check_array[manager.discount_permission],
                        })
                    return HttpResponse(managers_html)

        return HttpResponse('fail')


def get_orders(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:

                orders_html = ""
                orders = ShoppingLogic.get_user_purchases(username)
                for order in orders:
                    orders_html += loader.render_to_string('components/order.html', context={
                        'order_id': order.purchase_id,
                        'order_date': order.purchase_date,
                        'total_price': order.total_price,
                    })

                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
                navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
                return render(request, 'customer-orders.html',
                              context={'topbar': topbar, 'navbar': navbar, 'orders': orders_html})

        return HttpResponse('You are not logged in!')


def get_order(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        purchase_id = request.GET.get('order_id')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                items_html = ""
                items = ShoppingLogic.get_purchased_items_by_purchase_id(purchase_id)
                for item in items:
                    full_item = ItemsLogic.get_item(item.item_id)
                    items_html += loader.render_to_string('components/order.html', context={
                        'item_id': item.item_id,
                        'item_url': full_item.url,
                        'item_name': full_item.name,
                        'item_quantity': item.quantity,
                        'item_price': item.price,
                        'shop_name': full_item.shop_name,
                    })

                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
                navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
                return render(request, 'customer-order.html',
                              context={'topbar': topbar, 'navbar': navbar, 'items': items_html})

        return HttpResponse('You are not logged in!')


def get_system_shops(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_system_manager(username):
                    orders_html = ""
                    shops_html = ""
                    shops = ShopLogic.get_all_shops()
                    for shop in shops:
                        shops_html += loader.render_to_string('components/shop.html',
                                                              context={'shop_name': shop.name, 'status': shop.status})

                    topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                    cart_count = len(ShoppingLogic.get_cart_items(username))
                    navbar = loader.render_to_string('components/NavbarButtons.html',
                                                     context={'cart_items': cart_count})
                    return render(request, 'system-shops.html',
                                  context={'topbar': topbar, 'navbar': navbar, 'shops': shops_html})

        return HttpResponse("You don't have the privilege to be here")


def get_system_users(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_system_manager(username):
                    users_html = ""
                    users = UsersLogic.get_all_users()
                    for user in users:
                        shops_own = len(UsersLogic.get_owned_shops(user.username))
                        shop_manage = len(UsersLogic.get_managed_shops(user.username))

                        users_html += loader.render_to_string('components/user.html', context={
                            'username': user.username,
                            'shop_own_count': shops_own,
                            'shop_manage_count': shop_manage,
                        })

                    topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                    cart_count = len(ShoppingLogic.get_cart_items(username))
                    navbar = loader.render_to_string('components/NavbarButtons.html',
                                                     context={'cart_items': cart_count})
                    return render(request, 'system-users.html',
                                  context={'topbar': topbar, 'navbar': navbar, 'users': users_html})

        return HttpResponse("You don't have the privilege to be here")


def get_system_history(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_system_manager(username):
                    history_html = ""
                    purchased_items = ItemsLogic.get_all_purchased_items(username)
                    for purchased_item in purchased_items:
                        item = ItemsLogic.get_item(purchased_item.item_id)
                        purchase = ShoppingLogic.get_purchased_items_by_purchase_id(purchased_item.purchase_id)
                        history_html += loader.render_to_string('components/purchase_history.html',context={
                            'username':purchase.username,
                            'shop_name':item.shop_name,
                            'purchase_id':purchased_item.purchase_id,
                            'item_id': item.id,
                            'quantity': purchased_item.quantity,
                            'price':purchased_item.price
                        })

                    topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                    cart_count = len(ShoppingLogic.get_cart_items(username))
                    navbar = loader.render_to_string('components/NavbarButtons.html',
                                                     context={'cart_items': cart_count})
                    return render(request, 'system-history.html',
                                  context={'topbar': topbar, 'navbar': navbar,'history':history_html})

        return HttpResponse("You don't have the privilege to be here")
