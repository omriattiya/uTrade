from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingLogic, ItemsLogic
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from ServiceLayer import Consumer


@csrf_exempt
def remove_item_shopping_cart(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = Consumer.loggedInUsers.get(login)
        item_id = request.POST.get('item_id')
        status = ShoppingLogic.remove_item_shopping_cart(username, item_id)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def add_item_to_cart(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        item_id = int(request.POST.get('item_id'))
        quantity = int(request.POST.get('quantity'))
        status = ShoppingLogic.add_item_shopping_cart(ShoppingCartItem(Consumer.loggedInUsers.get(login), item_id, quantity, None))
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def add_item_shopping_cart(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        shop_cart = ShoppingCartItem(username, item_id, quantity, None)
        ShoppingLogic.add_item_shopping_cart(shop_cart)
        return HttpResponse('item added to cart')


@csrf_exempt
def update_item_shopping_cart(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = Consumer.loggedInUsers.get(login)
        item_id = int(request.POST.get("item_id"))
        new_quantity = int(request.POST.get("quantity"))
        status = ShoppingLogic.update_item_shopping_cart(username, item_id, new_quantity)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def update_code_shopping_cart(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = Consumer.loggedInUsers.get(login)
        code = request.POST.get("code")
        item = ItemsLogic.get_item_by_code(code)
        if item is False:
            return HttpResponse('fail')
        status = ShoppingLogic.update_code_shopping_cart(username, item.id, code)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


@csrf_exempt
def pay_all(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = Consumer.loggedInUsers.get(login)
        message = ShoppingLogic.pay_all(username)
        if message is True:
            return HttpResponse('OK')
        else:
            return HttpResponse(message)


def check_empty_cart(request):
    login = request.COOKIES.get('login_hash')
    username = Consumer.loggedInUsers.get(login)
    status = ShoppingLogic.check_empty_cart(username)
    if status is True:
        return HttpResponse('fail')
    else:
        return HttpResponse('OK')







