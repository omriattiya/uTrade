import hashlib

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from SharedClasses.VisibleDiscount import VisibleDiscount
from SharedClasses.InvisibleDiscount import InvisibleDiscount
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Owner import Owner
from SharedClasses.StoreManager import StoreManager
from SharedClasses.SystemManager import SystemManager
from DomainLayer import UsersLogic
from ServiceLayer import Consumer


def get_purchase_history(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        return UsersLogic.get_purchase_history(username)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = UsersLogic.register(RegisteredUser(username, password))
        if status:
            return HttpResponse('added successfully')
        else:
            return HttpResponse('failed')


@csrf_exempt
def remove_user(request):
    if request.method == 'POST':
        # return HttpResponse('user removed')
        username = request.POST.get('username')
        registered_user = request.POST.get('registered_user')
        UsersLogic.remove_user(username, registered_user)


@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        status = UsersLogic.edit_profile(RegisteredUser(username, new_password))
        if status:
            return HttpResponse('updated successfully')
        return HttpResponse('failed')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = RegisteredUser(username, password)
        if UsersLogic.login(user):
            access_token = hashlib.md5(username.encode()).hexdigest()
            Consumer.loggedInUsers[access_token] = username
            return HttpResponse(access_token)
        else:
            return HttpResponse('fail')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            if Consumer.loggedInUsers.get(login) is not None:
                del Consumer.loggedInUsers[login]
                return HttpResponse('success')

        return HttpResponse('fail')


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

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)

            if UsersLogic.add_owner(username, owner):
                return HttpResponse('success')
        return HttpResponse('fail')



@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')

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
                                         request.POST.get('get_discount_permission'))

            if UsersLogic.add_manager(username, store_manager):
                return HttpResponse('success')
        return HttpResponse('fail')


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
                                         request.POST.get('get_discount_permission'))

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
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if UsersLogic.modify_notifications(username, should_notify):
                return HttpResponse('success')
        return HttpResponse('fail')


def add_visible_discount(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        shop_name = request.POST.get('shop_name')
        percentage = request.POST.get('percentage')
        from_date = request.POST.get('from_date')
        end_date = request.POST.get('end_date')
        disc = VisibleDiscount(item_id, shop_name, percentage, from_date, end_date)
        username = request.POST.get('username')
        return UsersLogic.add_visible_discount(disc, username)


def add_invisible_discount(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        shop_name = request.POST.get('shop_name')
        percentage = request.POST.get('percentage')
        from_date = request.POST.get('from_date')
        end_date = request.POST.get('end_date')
        code = request.POST.get('code')
        disc = InvisibleDiscount(item_id, shop_name, percentage, from_date, end_date, code)
        username = request.POST.get('username')
        return UsersLogic.add_invisible_discount(disc, username)


def get_visible_discount(request):
    if request.method == 'GET':
        item_id = request.POST.get('item_id')
        shop_name = request.POST.get('shop_name')
        return UsersLogic.get_visible_discount(item_id, shop_name)


def get_invisible_discount(request):
    if request.method == 'GET':
        item_id = request.POST.get('item_id')
        shop_name = request.POST.get('shop_name')
        text = request.POST.get('text')
        return UsersLogic.get_invisible_discount(item_id, shop_name, text)


def add_system_manager(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        added_successfully = UsersLogic.add_system_manager(SystemManager(username, password))
        if added_successfully:
            return HttpResponse('added')
    return HttpResponse('failed - probably username exist in RegisteredUsers or SystemManagers')
