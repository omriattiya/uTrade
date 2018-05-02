from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingLogic
from DomainLayer.ItemsLogic import get_item
from SharedClasses.ShoppingCartItem import ShoppingCartItem


def remove_item_shopping_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        item_id = request.GET.get('itemId')
        ShoppingLogic.remove_item_shopping_cart(username, item_id)


def get_cart_items(request):
    if request.method == 'GET':
        #username = request.GET.get('username')
        username = 'OmriOmri'
        cart_items = ShoppingLogic.get_cart_items(username)
        items = []
        for i in [0,len(cart_items) - 1]:
            items.append(get_item(cart_items[i].item_id))
        if cart_items is not False:
            context = {'username': username, 'cart_items_combined': zip(cart_items,items)}
            return render(request, 'basket.html', context=context)


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
