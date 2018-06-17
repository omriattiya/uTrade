from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ItemsLogic
from DomainLayer import UserShoppingCartLogic, GuestShoppingCartLogic, LoggerLogic
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.ShoppingCartItem import ShoppingCartItem


@csrf_exempt
def remove_item_shopping_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        login = request.COOKIES.get('login_hash')
        if login is not None and Consumer.loggedInUsers.get(login) is None:
            status = UserShoppingCartLogic.remove_item_shopping_cart(login, item_id)
        else:
            guest = request.COOKIES.get('guest_hash')
            if guest is None:
                return HttpResponse('fail')
            status = GuestShoppingCartLogic.remove_item_shopping_cart_guest(guest, item_id)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def add_item_to_cart(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('item_id'))
        quantity = int(request.POST.get('quantity'))
        item = ItemsLogic.get_item(item_id)
        if item.quantity < quantity:
            return HttpResponse('Stock_Error')
        login = request.COOKIES.get('login_hash')
        if login is None:
            login = request.POST.get('login_hash')
        if login is not None and Consumer.loggedInUsers.get(login) is not None:
            username = Consumer.loggedInUsers.get(login)
            status = UserShoppingCartLogic.add_item_shopping_cart(login, ShoppingCartItem(username, item_id, quantity, None))
            if status is False:
                return HttpResponse('fail')
            else:
                return HttpResponse('OK')
        else:
            if item.kind == 'ticket':
                return HttpResponse('guest ticket')
            guest = request.COOKIES.get('guest_hash')
            if guest is None:
                guest = 'guest' + Consumer.guestIndex
                Consumer.guestIndex += 1
            status = GuestShoppingCartLogic.add_guest_item_shopping_cart(guest, item_id, quantity)
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
        if login is None or Consumer.loggedInUsers.get(login) is None:
            guest = request.COOKIES.get('guest_hash')
            if guest is None:
                return HttpResponse('fail')
            status = GuestShoppingCartLogic.update_item_shopping_cart_guest(guest, item_id, new_quantity)
        else:
            status = UserShoppingCartLogic.update_item_shopping_cart(login, item_id, new_quantity)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def update_code_shopping_cart(request):
    if request.method == 'POST':
        code = request.POST.get("code")

        event = "UPDATE CODE SHOPPING CART"
        suspect_sql_injection = LoggerLogic.identify_sql_injection(code, event)

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        item = ItemsLogic.get_item_by_code(code)
        if item is False:
            return HttpResponse('fail')
        login = request.COOKIES.get('login_hash')
        if login is None or Consumer.loggedInUsers.get(login) is None:
            guest = request.COOKIES.get('guest_hash')
            if guest is None:
                return HttpResponse('fail')
            status = GuestShoppingCartLogic.update_code_shopping_cart_guest(guest, item.id, code)
        else:
            status = UserShoppingCartLogic.update_code_shopping_cart(login, item.id, code)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def pay_all(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        if login is None:
            login = request.POST.get('login_hash')
        if login is None or Consumer.loggedInUsers.get(login) is None:
            guest = request.COOKIES.get('guest_hash')
            if guest is None:
                return HttpResponse('fail')
            username = 'GUEST'
            message = GuestShoppingCartLogic.pay_all_guest(guest)
        else:
            username = Consumer.loggedInUsers.get(login)
            message = UserShoppingCartLogic.pay_all(login)
        if isinstance(message, list):
            to_send = 'OK' + str(message[0]) + '}' + str(message[1])
            return HttpResponse(to_send)
        else:
            LoggerLogic.add_error_log(username, "PAY ALL", message)
            return HttpResponse(message)


def check_valid_cart(request):
    login = request.COOKIES.get('login_hash')
    if login is None or Consumer.loggedInUsers.get(login) is None:
        guest = request.COOKIES.get('guest_hash')
        if guest is None:
            return HttpResponse('fail')
        status = GuestShoppingCartLogic.check_empty_cart_guest(guest)
        if not status:
            status = GuestShoppingCartLogic.check_valid_cart(guest)
            if status is True:
                return HttpResponse('OK')
            else:
                return HttpResponse(status)
        else:
            return HttpResponse('fail')
    else:
        status = UserShoppingCartLogic.check_empty_cart_user(login)
        if not status:
            status = UserShoppingCartLogic.check_valid_cart(login)
            if status is True:
                return HttpResponse('OK')
            else:
                return HttpResponse(status)
        else:
            return HttpResponse('fail')
