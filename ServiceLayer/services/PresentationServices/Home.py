from django.shortcuts import render

from DomainLayer import SearchLogic
from ServiceLayer.services.PresentationServices import Topbar_Navbar


def get_home(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        items = SearchLogic.get_top_five_ranked_items()
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest), 'items':items}
        return render(request, 'index.html', context=context)


def get_register(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        guest = request.COOKIES.get('guest_hash')
        context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
        return render(request, 'register.html', context=context)
