from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ShoppingPolicyLogic
from ServiceLayer.services.LiveAlerts import Consumer


#    ____________________________________   GET ALL     ___________________________________________________


def get_all_shopping_policy_on_shop(request):
    if request.method == 'GET':
        return ShoppingPolicyLogic.get_all_shopping_policy_on_shop()
    return HttpResponse('FAILED')


def get_all_shopping_policy_on_items(request):
    if request.method == 'GET':
        return ShoppingPolicyLogic.get_all_shopping_policy_on_items()
    return HttpResponse('FAILED')


def get_all_shopping_policy_on_identity(request):
    if request.method == 'GET':
        return ShoppingPolicyLogic.get_all_shopping_policy_on_identity()
    return HttpResponse('FAILED')


def get_all_shopping_policy_on_category(request):
    if request.method == 'GET':
        return ShoppingPolicyLogic.get_all_shopping_policy_on_category()
    return HttpResponse('FAILED')


#    ____________________________________   INSERT     ___________________________________________________

@csrf_exempt
def add_shopping_policy_on_items(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            item_name = request.POST.get('item_name')
            conditions = request.POST.get('conditions')
            restriction = request.POST.get('restriction')
            quantity = request.POST.get('quantity')
            status = ShoppingPolicyLogic.add_shopping_policy_on_items(username, item_name, conditions, restriction, quantity)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def add_shopping_policy_on_category(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            category = request.POST.get('category')
            conditions = request.POST.get('conditions')
            restriction = request.POST.get('restriction')
            quantity = request.POST.get('quantity')
            status = ShoppingPolicyLogic.add_shopping_policy_on_category(username, category, conditions, restriction, quantity)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def add_shopping_policy_on_shop(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            shop_name = request.POST.get('shop_name')
            conditions = request.POST.get('conditions')
            restriction = request.POST.get('restriction')
            quantity = request.POST.get('quantity')
            status = ShoppingPolicyLogic.add_shopping_policy_on_shop(username, shop_name, conditions, restriction, quantity)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def add_shopping_policy_on_identity(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            conditions = request.POST.get('conditions')
            restriction = request.POST.get('restriction')
            quantity = request.POST.get('quantity')
            status = ShoppingPolicyLogic.add_shopping_policy_on_identity(username, conditions, restriction, quantity)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


#    ____________________________________   DELETE     ___________________________________________________

@csrf_exempt
def remove_shopping_policy_on_identity(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            status = ShoppingPolicyLogic.remove_shopping_policy_on_identity(username, policy_id)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def remove_shopping_policy_on_shop(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            shop_name = request.POST.get('shop_name')
            status = ShoppingPolicyLogic.remove_shopping_policy_on_shop(username, policy_id, shop_name)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def remove_shopping_policy_on_items(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            status = ShoppingPolicyLogic.remove_shopping_policy_on_items(username, policy_id)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def remove_shopping_policy_on_category(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            status = ShoppingPolicyLogic.remove_shopping_policy_on_category(username, policy_id)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


#    ____________________________________   UPDATE     ___________________________________________________


@csrf_exempt
def update_shopping_policy_on_identity(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            field_name = request.POST.get('field_name')
            new_value = request.POST.get('new_value')
            status = ShoppingPolicyLogic.update_shopping_policy_on_identity(username, policy_id, field_name, new_value)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def update_shopping_policy_on_shop(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: you are not logged in')
            policy_id = request.POST.get('policy_id')
            field_name = request.POST.get('field_name')
            new_value = request.POST.get('new_value')
            shop_name = request.POST.get('shop_name')
            status = ShoppingPolicyLogic.update_shopping_policy_on_shop(username, policy_id, field_name, new_value, shop_name)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def update_shopping_policy_on_items(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            field_name = request.POST.get('field_name')
            new_value = request.POST.get('new_value')
            status = ShoppingPolicyLogic.update_shopping_policy_on_items(username, policy_id, field_name, new_value)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')


@csrf_exempt
def update_shopping_policy_on_category(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('FAILED: username is None')
            policy_id = request.POST.get('policy_id')
            field_name = request.POST.get('field_name')
            new_value = request.POST.get('new_value')
            status = ShoppingPolicyLogic.update_shopping_policy_on_category(username, policy_id, field_name, new_value)
            if status is not True:
                return HttpResponse(status)
            return HttpResponse('SUCCESS')
        return HttpResponse('FAILED: you are not logged in!')
    return HttpResponse('FAILED: not a POST request')
