from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingLogic, ItemsLogic
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from ServiceLayer import Consumer


@csrf_exempt
def remove_item_shopping_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                guest = request.COOKIES.get('guest_hash')
                status = ShoppingLogic.remove_item_shopping_cart_guest(guest, item_id)
            else:
                status = ShoppingLogic.remove_item_shopping_cart(username, item_id)
        else:
            guest = request.COOKIES.get('guest_hash')
            status = ShoppingLogic.remove_item_shopping_cart_guest(guest, item_id)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def add_item_to_cart(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('item_id'))
        quantity = int(request.POST.get('quantity'))
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                status = ShoppingLogic.add_item_shopping_cart(ShoppingCartItem(username, item_id, quantity, None))
                if status is False:
                    return HttpResponse('fail')
                else:
                    return HttpResponse('OK')
            else:
                guest = request.COOKIES.get('guest_hash')
                if guest is None:
                    guest = ShoppingLogic.get_new_guest_name()
                if guest is False:
                    return HttpResponse('fail')
                status = ShoppingLogic.add_guest_item_shopping_cart(guest, item_id, quantity)
                if status is False:
                    return HttpResponse('fail')
                else:
                    string_guest = str(guest)
                    return HttpResponse(string_guest)
        else:
            guest = request.COOKIES.get('guest_hash')
            if guest is None:
                guest = ShoppingLogic.get_new_guest_name()
            if guest is False:
                return HttpResponse('fail')
            status = ShoppingLogic.add_guest_item_shopping_cart(guest, item_id, quantity)
            if status is False:
                return HttpResponse('fail')
            else:
                string_guest = str(guest)
                return HttpResponse(string_guest)



@csrf_exempt
def update_item_shopping_cart(request):
    if request.method == 'POST':
        item_id = int(request.POST.get("item_id"))
        new_quantity = int(request.POST.get("quantity"))
        login = request.COOKIES.get('login_hash')
        if login is None:
            guest = request.COOKIES.get('guest_hash')
            status = ShoppingLogic.update_item_shopping_cart_guest(guest, item_id, new_quantity)
        else:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                status = ShoppingLogic.update_item_shopping_cart(username, item_id, new_quantity)
            else:
                guest = request.COOKIES.get('guest_hash')
                status = ShoppingLogic.update_item_shopping_cart_guest(guest, item_id, new_quantity)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def update_code_shopping_cart(request):
    if request.method == 'POST':
        code = request.POST.get("code")
        item = ItemsLogic.get_item_by_code(code)
        if item is False:
            return HttpResponse('fail')
        login = request.COOKIES.get('login_hash')
        if login is None:
            guest = request.COOKIES.get('guest_hash')
            status = ShoppingLogic.update_code_shopping_cart_guest(guest, item.id, code)
        else:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                status = ShoppingLogic.update_code_shopping_cart(username, item.id, code)
            else:
                guest = request.COOKIES.get('guest_hash')
                status = ShoppingLogic.update_code_shopping_cart_guest(guest, item.id, code)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def pay_all(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is None:
            guest = request.COOKIES.get('guest_hash')
            message = ShoppingLogic.pay_all_guest(guest)
        else:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                message = ShoppingLogic.pay_all(username)
            else:
                guest = request.COOKIES.get('guest_hash')
                message = ShoppingLogic.pay_all_guest(guest)
        if message is True:
            return HttpResponse('OK')
        else:
            return HttpResponse(message)


def check_empty_cart(request):
    login = request.COOKIES.get('login_hash')
    if login is None:
        guest = request.COOKIES.get('guest_hash')
        status = ShoppingLogic.check_empty_cart_guest(guest)
    else:
        username = Consumer.loggedInUsers.get(login)
        if username is not None:
            status = ShoppingLogic.check_empty_cart_user(username)
        else:
            guest = request.COOKIES.get('guest_hash')
            status = ShoppingLogic.check_empty_cart_guest(guest)
    if status is True:
        return HttpResponse('fail')
    else:
        return HttpResponse('OK')







