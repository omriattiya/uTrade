from django.shortcuts import render
from DomainLayer import UserShoppingCartLogic, GuestShoppingCartLogic
from ExternalSystems import PaymentSystem, SupplySystem, ExternalSystems
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar


def review_order(request):
    if request.method == 'GET':
        return render(request, 'checkout4.html', context=shopping_cart_items_helper(request))


def get_cart_items(request):
    if request.method == 'GET':
        return render(request, 'basket.html', context=shopping_cart_items_helper(request))


def address(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
        return render(request, 'checkout1.html', context=context)


def show_receipt(request):
    if request.method == 'GET':
        name = ''
        purchase_id = request.GET.get("purchase_id")
        amount = request.GET.get("amount")
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                name = username
            else:
                if guest is not None:
                    name = guest
        else:
            if guest is not None:
                name = guest
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
        payment = ExternalSystems.payment.pay(float(amount), name)
        delivery = ExternalSystems.supply.supply_a_purchase(name, int(purchase_id))
        context['payment'] = payment
        context['delivery'] = delivery
        return render(request, 'receipt.html', context=context)


def shopping_cart_items_helper(request):
    login = request.COOKIES.get('login_hash')
    guest = request.COOKIES.get('guest_hash')
    context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
    if login is not None:
        username = Consumer.loggedInUsers.get(login)
        if username is not None:
            context.update(UserShoppingCartLogic.order_of_user(login))
        else:
            if guest is not None:
                context.update(GuestShoppingCartLogic.order_of_guest(guest))
    else:
        if guest is not None:
            context.update(GuestShoppingCartLogic.order_of_guest(guest))
    return context
