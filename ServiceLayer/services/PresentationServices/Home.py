from django.shortcuts import render
from django.template import loader

from DomainLayer import SearchLogic
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar
from ServiceLayer.services.PresentationServices.Shop import item_discount, category_discount


def get_home(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        items = SearchLogic.get_top_five_ranked_items()
        for item in items:
            shop_name = item.shop_name
            item.price = (round(item.price * item_discount(item.id, shop_name) * category_discount(item.category,
                                                                                                   shop_name), 2))
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest),
                   'items': items}
        return render(request, 'index.html', context=context)


def get_register(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
        return render(request, 'register.html', context=context)
