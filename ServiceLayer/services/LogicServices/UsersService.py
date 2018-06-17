import hashlib

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import UserShoppingCartLogic, LoggerLogic
from DomainLayer import UsersLogic, ShoppingLogic, DiscountLogic
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.Owner import Owner
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.StoreManager import StoreManager
from SharedClasses.SystemManager import SystemManager


def get_purchase_history(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        return UsersLogic.get_purchase_history(username)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        state = request.POST.get('state')
        age = request.POST.get('age')
        sex = request.POST.get('sex')

        event = "REGISTER"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(username, event)
        suspect_sql_injection = LoggerLogic.identify_sql_injection(password, event)
        suspect_sql_injection = LoggerLogic.identify_sql_injection(state, event)
        suspect_sql_injection = LoggerLogic.identify_sql_injection(age, event)
        suspect_sql_injection = LoggerLogic.identify_sql_injection(sex, event)

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        return HttpResponse(UsersLogic.register_with_user_detail(RegisteredUser(username, password), state, age, sex))


@csrf_exempt
def remove_user(request):
    if request.method == 'POST':
        registered_user = request.POST.get('registered_user')

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)

            if UsersLogic.remove_user(username, RegisteredUser(registered_user, None)):
                for k, v in Consumer.loggedInUsers.items():
                    if v == registered_user:
                        del Consumer.loggedInUsers[k]
                        del Consumer.loggedInUsersShoppingCart[k]
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def edit_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        event = "EDIT PASSWORD"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(current_password, event)
        suspect_sql_injection = LoggerLogic.identify_sql_injection(new_password, event)

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)

            if UsersLogic.login(RegisteredUser(username, current_password)):
                return HttpResponse(UsersLogic.edit_password(RegisteredUser(username, new_password)))

        return HttpResponse('FAILED: You are not logged in.')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        event = "LOGIN"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(username, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(password, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        user = RegisteredUser(username, password)
        result = UsersLogic.login(user)
        if result[:7] == 'SUCCESS':
            access_token = hashlib.md5(username.encode()).hexdigest()
            Consumer.loggedInUsers[access_token] = username
            Consumer.loggedInUsersShoppingCart[access_token] = ShoppingLogic.get_cart_items(username)
            return HttpResponse(access_token)
        else:
            return HttpResponse(result)


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            if Consumer.loggedInUsers.get(login) is not None:
                UserShoppingCartLogic.remove_shopping_cart_db(Consumer.loggedInUsers.get(login))
                UserShoppingCartLogic.add_all_shopping_cart_to_user(Consumer.loggedInUsersShoppingCart[login])
                del Consumer.loggedInUsers[login]
                del Consumer.loggedInUsersShoppingCart[login]
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def update_details(request):
    if request.method == 'POST':
        state = request.POST.get('state')
        age = request.POST.get('age')
        sex = request.POST.get('sex')

        event = "UPDATE USER DETAILS"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(state, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(age, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(sex, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            return HttpResponse(UsersLogic.update_details(username, state, age, sex))

        return HttpResponse('FAILED: You are not logged in.')


# _____
#   / ___ \
#  | |   | | _ _ _  ____    ____   ____   ___
#  | |   | || | | ||  _ \  / _  ) / ___) /___)
#  | |___| || | | || | | |( (/ / | |    |___ |
#   \_____/  \____||_| |_| \____)|_|    (___/
#

@csrf_exempt
def add_owner(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')
        owner = Owner(target_id, shop_name, None)

        event = "ADD OWNER"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(target_id, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            return HttpResponse(UsersLogic.add_owner(username, owner))
        return HttpResponse('FAILED: You are not logged in')


@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')

        event = "ADD MANAGER"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(target_id, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)

            store_manager = StoreManager(target_id, shop_name,
                                         request.POST.get('add_item_permission'),
                                         request.POST.get('remove_item_permission'),
                                         request.POST.get('edit_item_permission'),
                                         request.POST.get('reply_message_permission'),
                                         request.POST.get('get_all_message_permission'),
                                         request.POST.get('get_purchase_history_permission'),
                                         request.POST.get('get_discount_permission'),
                                         request.POST.get('set_policy_permission'))

            if username is not None:
                return HttpResponse(UsersLogic.add_manager(username, store_manager))
        return HttpResponse('FAILED: You are not logged in')


@csrf_exempt
def remove_manager(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)

            if UsersLogic.remove_store_manager(username, shop_name, target_id):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def update_permissions(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')

        event = "UPDATE PERMISSIONS"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(target_id, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)

            store_manager = StoreManager(target_id, shop_name,
                                         request.POST.get('add_item_permission'),
                                         request.POST.get('remove_item_permission'),
                                         request.POST.get('edit_item_permission'),
                                         request.POST.get('reply_message_permission'),
                                         request.POST.get('get_all_message_permission'),
                                         request.POST.get('get_purchase_history_permission'),
                                         request.POST.get('get_discount_permission'),
                                         request.POST.get('set_policy_permission'))

            if UsersLogic.update_permissions(username, store_manager):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def close_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if UsersLogic.close_shop(username, shop_name):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def re_open_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if UsersLogic.re_open_shop(username, shop_name):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def modify_notifications(request):
    if request.method == 'POST':
        should_notify = request.POST.get('modify_notifications')
        shop_name = request.POST.get('shop_name')

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if UsersLogic.modify_notifications(username, should_notify, shop_name):
                return HttpResponse('success')
        return HttpResponse('fail')


def get_visible_discount(request):
    if request.method == 'GET':
        item_id = request.POST.get('item_id')
        shop_name = request.POST.get('shop_name')
        return DiscountLogic.get_visible_discount(item_id, shop_name)


def get_invisible_discount(request):
    if request.method == 'GET':
        item_id = request.POST.get('item_id')
        shop_name = request.POST.get('shop_name')
        text = request.POST.get('text')
        return DiscountLogic.get_invisible_discount(item_id, shop_name, text)


def add_system_manager(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        event = "ADD VISIBLE DISCOUNT"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(username, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(password, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        added_successfully = UsersLogic.add_system_manager(SystemManager(username, password))
        if added_successfully:
            return HttpResponse('added')
    return HttpResponse('failed - probably username exist in RegisteredUsers or SystemManagers')


@csrf_exempt
def clear_alerts(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            box = Consumer.user_alerts_box.get(username)
            if box is None:
                return HttpResponse('You have no alerts')
            del Consumer.user_alerts_box[username]
            return HttpResponse('success')
        return HttpResponse('fail')
