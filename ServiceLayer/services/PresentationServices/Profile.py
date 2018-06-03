from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import UsersLogic, ShopLogic, ShoppingLogic, ItemsLogic, HistoryAppointingLogic, ShoppingPolicyLogic
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar
from SharedClasses.Item import Item


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
                    details = {'state': "AFG",
                               'age': "AFG",
                               'sex': "AFG"}
                else:
                    details = UsersLogic.get_user_details(username)
                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'system_hidden': system_hidden,
                                'state': details.get('state'),
                                'age': details.get('age'),
                                'sex': details.get('sex')})
                return render(request, 'customer-account.html',
                              context=context)

        return HttpResponse('You are not logged in!')


def get_shops(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                owned_shops_html = ""
                owned_shops = UsersLogic.get_owned_shops(username)
                for owned_shop in owned_shops:
                    shop = ShopLogic.search_shop(owned_shop.shop_name)
                    rank = ShopLogic.get_shop_rank(shop.name)
                    checked = ""
                    if owned_shop.should_notify > 0:
                        checked = 'checked="checked"'

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
                        'SP': yes_no_array[managed_shop.permission_set_policy],
                        'checked': checked
                    })
                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'owned_shops': owned_shops_html, 'managed_shops': managed_shops_html})
                return render(request, 'customer-shops.html', context=context)

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
                            'checked_SP': check_array[manager.permission_set_policy],
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
                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'orders': orders_html})
                return render(request, 'customer-orders.html', context=context)
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
                    items_html += loader.render_to_string('components/PurchasedItem.html', context={
                        'item_id': item.item_id,
                        'item_url': full_item.url,
                        'item_name': full_item.name,
                        'item_quantity': item.quantity,
                        'item_price': item.price,
                        'shop_name': full_item.shop_name,
                    })
                date = ShoppingLogic.get_purchase(purchase_id).purchase_date
                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'items': items_html, 'order_id': purchase_id,
                                'order_date': date})
                return render(request, 'customer-order.html', context=context)
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

                    context = {'topbar': Topbar_Navbar.get_top_bar(login),
                               'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                    context.update({'shops': shops_html})
                    return render(request, 'system-shops.html', context=context)
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
                    context = {'topbar': Topbar_Navbar.get_top_bar(login),
                               'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                    context.update({'users': users_html})
                    return render(request, 'system-users.html', context=context)
        return HttpResponse("You don't have the privilege to be here")


def get_system_policies(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                if UsersLogic.is_system_manager(username):
                    item_policies_html = ""
                    item_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_items()
                    for item_policy in item_policies:
                        is_none = ""
                        selectors = {}
                        if item_policy.restriction is 'N':
                            is_none = "disabled"
                        selectors['N'] = ""
                        selectors['UT'] = ""
                        selectors['AL'] = ""
                        selectors['E'] = ""
                        selectors[item_policy.restriction] = 'selected="selected"'

                        item_policies_html += loader.render_to_string('components/shopping_item_policy.html', context={
                            'id': item_policy.policy_id,
                            'item_name': item_policy.item_name,
                            'selector_value': item_policy.restriction,
                            'quantity': item_policy.quantity,
                            'is_none': is_none,
                            'N_S': selectors.get('N'),
                            'UT_S': selectors.get('UT'),
                            'AL_S': selectors.get('AL'),
                            'E_S': selectors.get('E'),
                        })

                    category_policies_html = ""
                    category_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_category()
                    for category_policy in category_policies:
                        is_none = ""
                        selectors = {}
                        if category_policy.restriction is 'N':
                            is_none = "disabled"
                        selectors['N'] = ""
                        selectors['UT'] = ""
                        selectors['AL'] = ""
                        selectors['E'] = ""
                        selectors[category_policy.restriction] = 'selected="selected"'

                        category_policies_html += loader.render_to_string('components/shopping_category_policy.html',
                                                                          context={
                                                                              'id': category_policy.policy_id,
                                                                              'category_name': category_policy.category,
                                                                              'selector_value': category_policy.restriction,
                                                                              'quantity': category_policy.quantity,
                                                                              'is_none': is_none,
                                                                              'N_S': selectors.get('N'),
                                                                              'UT_S': selectors.get('UT'),
                                                                              'AL_S': selectors.get('AL'),
                                                                              'E_S': selectors.get('E'),
                                                                          })

                    global_policies_html = ""
                    global_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_identity()
                    for global_policy in global_policies:
                        is_none = ""
                        selectors = {}
                        if global_policy.restriction is 'N':
                            is_none = "disabled"
                        selectors['N'] = ""
                        selectors['UT'] = ""
                        selectors['AL'] = ""
                        selectors['E'] = ""
                        selectors[global_policy.restriction] = 'selected="selected"'

                        global_policies_html += loader.render_to_string('components/shopping_global_policy.html',
                                                                        context={
                                                                            'id': global_policy.policy_id,
                                                                            'selector_value': global_policy.restriction,
                                                                            'quantity': global_policy.quantity,
                                                                            'is_none': is_none,
                                                                            'N_S': selectors.get('N'),
                                                                            'UT_S': selectors.get('UT'),
                                                                            'AL_S': selectors.get('AL'),
                                                                            'E_S': selectors.get('E'),
                                                                        })

                    topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                    cart_count = len(ShoppingLogic.get_cart_items(username))
                    navbar = loader.render_to_string('components/NavbarButtons.html',
                                                     context={'cart_items': cart_count})
                    return render(request, 'system-policies.html',
                                  context={'topbar': topbar, 'navbar': navbar,
                                           'item_policies': item_policies_html,
                                           'category_policies': category_policies_html,
                                           'global_policies': global_policies_html})

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
                        if item is False:
                            item = Item(purchased_item.item_id, None, None, None, None, None, None, None, None, 0, 0, 0)
                        purchase = ShoppingLogic.get_purchase(purchased_item.purchase_id)
                        history_html += loader.render_to_string('components/purchase_history.html', context={
                            'username': purchase.username,
                            'shop_name': item.shop_name,
                            'purchase_id': purchased_item.purchase_id,
                            'item_id': item.id,
                            'quantity': purchased_item.quantity,
                            'price': purchased_item.price
                        })

                    context = {'topbar': Topbar_Navbar.get_top_bar(login),
                               'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                    context.update({'history': history_html})
                    return render(request, 'system-history.html', context=context)
        return HttpResponse("You don't have the privilege to be here")


def get_history_appoitings(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')

        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                shop_name = request.GET.get('shop_name')
                history = HistoryAppointingLogic.get_history_apppoitings(shop_name)
                history_html = ''
                for hist in history:
                    history_html += loader.render_to_string('components/historyappointings.html', context={
                        'appointing_user': hist.appointing_user,
                        'appointed_user': hist.appointed_user,
                        'position': hist.position,
                        'date': hist.date,
                        'permissions': hist.permissions,
                    })
                return HttpResponse(history_html)
    return HttpResponse('fail')
