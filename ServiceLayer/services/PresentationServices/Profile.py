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
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
                navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
                return render(request, 'customer-account.html', context={'topbar': topbar, 'navbar': navbar})

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
                    orders_html += loader.render_to_string('components/Order.html', context={
                        'order_id': order.purchase_id,
                        'order_date': order.purchase_date,
                        'total_price': order.total_price,
                    })

                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
                navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
                return render(request, 'customer-orders.html', context={'topbar': topbar, 'navbar': navbar,'orders':orders_html})

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
                    items_html += loader.render_to_string('components/Order.html', context={
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
                return render(request, 'customer-order.html', context={'topbar': topbar, 'navbar': navbar,'items':items_html})

        return HttpResponse('You are not logged in!')