from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from SharedClasses.RegisteredUser import RegisteredUser
from DomainLayer import UsersLogic


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
        return HttpResponse('user removed')


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
        shop_id = request.POST.get('shop_id')
        target_id = request.POST.get('target_id')
        return UsersLogic.add_owner(username, shop_id, target_id)


@csrf_exempt
def add_manager(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        shop_id = request.POST.get('shop_id')
        target_id = request.POST.get('target_id')
        permissions = {"addItemPermission": request.POST.get('addItemPermission'),
                       "editItemPermission": request.POST.get('editItemPermission'),
                       "replyMessagePermission": request.POST.get('replyMessagePermission'),
                       "getAllMessagePermission": request.POST.get('getAllMessagePermission'),
                       "getPurchaseHistoryPermission": request.POST.get('getPurchaseHistoryPermission')}
        return UsersLogic.add_manager(username, shop_id, target_id, permissions)
