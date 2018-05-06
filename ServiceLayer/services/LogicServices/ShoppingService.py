from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingLogic, ItemsLogic
from DomainLayer.ItemsLogic import get_item
from DomainLayer.UsersLogic import get_visible_discount, get_invisible_discount
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from ServiceLayer import Consumer


@csrf_exempt
def remove_item_shopping_cart(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        item_id = request.POST.get('item_id')
        status = ShoppingLogic.remove_item_shopping_cart(username, item_id)
        if status is False:
            return HttpResponse('Removing Item Failed')
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


def get_cart_items(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        cart_count = 0
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        context = order_helper(Consumer.loggedInUsers.get(login))
        context['topbar'] = topbar
        context['navbar'] = navbar
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
        code = request.POST.get("code")
        item = ItemsLogic.get_item_by_code(code)
        status = ShoppingLogic.update_code_shopping_cart(username, item.id, code)
        if status is False:
            return HttpResponse('Removing Item Failed')
        else:
            return HttpResponse('OK')


@csrf_exempt
def pay_all(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = Consumer.loggedInUsers.get(login)
        # return HttpResponse('item added to cart')
        status = ShoppingLogic.pay_all(username)
        if status is False:
            return HttpResponse('fail')
        else:
            return HttpResponse('OK')


def address(request):
    if request.method == 'GET':
        username = 'OmriOmri'
        context = {'username': username}
        return render(request, 'checkout1.html', context=context)


def deliver(request):
    if request.method == 'GET':
        username = 'OmriOmri'
        context = {'username': username}
        return render(request, 'checkout2.html', context=context)


def payment_method(request):
    if request.method == 'GET':
        username = 'OmriOmri'
        context = {'username': username}
        return render(request, 'checkout3.html', context=context)


def review_order(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        cart_count = 0
        topbar = loader.render_to_string('components/Topbar.html', context=None)
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                topbar = loader.render_to_string('components/TopbarLoggedIn.html', context={'username': username})
                cart_count = len(ShoppingLogic.get_cart_items(username))
        navbar = loader.render_to_string('components/NavbarButtons.html', context={'cart_items': cart_count})
        context = order_helper(Consumer.loggedInUsers.get(login))
        context['topbar'] = topbar
        context['navbar'] = navbar
        username = Consumer.loggedInUsers.get(login)
        context['username'] = username
        return render(request, 'checkout4.html', context=context)


def order_helper(username):
    # username = request.GET.get('username')
    if username is None:
        cart_items = ShoppingLogic.get_cart_items_by_cookies()
    else:
        cart_items = ShoppingLogic.get_cart_items(username)
    items = []
    discount_prices = []
    total_prices = []
    context = {}
    if len(cart_items) == 0:
        return {'username': username, 'total_price': 0, 'cart_items_combined': cart_items}
    else:
        total_price = 0
        for i in [0, len(cart_items) - 1]:
            item = get_item(cart_items[i].item_id)
            visible_discount = get_visible_discount(item.id, item.shop_name)
            percentage_visible = 0
            percentage_invisible = 0
            if visible_discount is not False:
                percentage_visible = visible_discount.percentage
            if cart_items[i].code is not None:
                invisible_discount = get_invisible_discount(item.id, item.shop_name, cart_items[i].code)
                percentage_invisible = invisible_discount.percentage
            discount_money = percentage_visible * item.price + percentage_invisible * (
                        1 - percentage_visible) * item.price
            discount_prices.append(discount_money)
            items.append(item)
            total_prices.append(item.price * cart_items[i].item_quantity - discount_money * cart_items[i].item_quantity)
            total_price = total_price + item.price * cart_items[i].item_quantity - discount_money * cart_items[
                i].item_quantity
        if cart_items is not False:
            return {'username': username, 'total_price': total_price,
                    'cart_items_combined': zip(cart_items, items, discount_prices, total_prices)}
