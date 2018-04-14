from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingLogic
from SharedClasses.ShoppingCart import ShoppingCart

def remove_item_shopping_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        item_id = request.GET.get('itemId')
        ShoppingLogic.remove_item_shopping_cart(username, item_id)


def get_cart_items(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        ShoppingLogic.get_cart_items(username)


@csrf_exempt
def add_item_shopping_cart(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        shop_cart = ShoppingCart(username,item_id,quantity,None)
        ShoppingLogic.add_item_shopping_cart(shop_cart)
        return HttpResponse('item added to cart')


@csrf_exempt
def update_item_shopping_cart(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        item_id = request.POST.get("item_id")
        new_quantity = request.POST.get("new_quantity")
        return ShoppingLogic.update_item_shopping_cart(username, item_id, new_quantity)


@csrf_exempt
def update_code_shopping_cart(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        item_id = request.POST.get("item_id")
        code = request.POST.get("code")
        return ShoppingLogic.update_code_shopping_cart(username, item_id, code)


@csrf_exempt
def pay_all(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # return HttpResponse('item added to cart')
        return ShoppingLogic.pay_all(username)
