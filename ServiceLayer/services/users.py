from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from SharedClasses.VisibleDiscount import VisibleDiscount
from SharedClasses.InvisibleDiscount import InvisibleDiscount
from SharedClasses.RegisteredUser import RegisteredUser
from DomainLayer import UsersLogic


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
        return UsersLogic.login(user)


#    _____
#   / ___ \
#  | |   | | _ _ _  ____    ____   ____   ___
#  | |   | || | | ||  _ \  / _  ) / ___) /___)
#  | |___| || | | || | | |( (/ / | |    |___ |
#   \_____/  \____||_| |_| \____)|_|    (___/
#

@csrf_exempt
def add_owner(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')
        return UsersLogic.add_owner(username, shop_name, target_id)


@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        shop_name = request.POST.get('shop_name')
        target_id = request.POST.get('target_id')
        permissions = {"addItemPermission": request.POST.get('addItemPermission'),
                       "editItemPermission": request.POST.get('editItemPermission'),
                       "replyMessagePermission": request.POST.get('replyMessagePermission'),
                       "getAllMessagePermission": request.POST.get('getAllMessagePermission'),
                       "getPurchaseHistoryPermission": request.POST.get('getPurchaseHistoryPermission')}
        return UsersLogic.add_manager(username, shop_name, target_id, permissions)


@csrf_exempt
def close_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        return UsersLogic.close_shop(shop_name)


def re_open_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        return UsersLogic.re_open_shop(shop_name)


def modify_notifications(request):
    if request.method == 'POST':
        should_notify = request.POST.get('modify_notifications')
        owner_id = request.POST.get('modify_notifications')
        return UsersLogic.modify_notifications(owner_id, should_notify)


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
        added_successfully = UsersLogic.add_system_manager(username, password)
        if added_successfully:
            return HttpResponse('added')
    return HttpResponse('failed - probably username exist in RegisteredUsers or SystemManagers')
