from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ItemsLogic
from DomainLayer import ShopLogic
from SharedClasses import Shop
from DatabaseLayer import Shops


@csrf_exempt
def create_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        shop_id = request.POST.get('id')
        shop_title = request.POST.get('title')
        shop_rank = request.POST.get('rank')
        shop_status = request.POST.get('status')
        user_id = request.POST.get('user_id')
        shop = Shop(shop_id, shop_title, shop_rank, shop_status)
        Shops.create_shop(shop, user_id)


@csrf_exempt
def remove_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('item_id')
        ItemsLogic.remove_item_from_shop(item_id)


@csrf_exempt
def add_review_on_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        writer_id = request.POST.get('writer_id')
        shop_id = request.POST.get('shop_id')
        description = request.POST.get('description')
        rank = request.POST.get('rank')
        Shops.add_review_on_shop(writer_id, shop_id, description, rank)


def get_shop_purchase_history(request):
    if request.method == 'GET':
        return HttpResponse('no GUI yet')


@csrf_exempt
def close_shop_permanently(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        shop_id = request.POST.get('shop_id')
        # return HttpResponse('no GUI yet')
        ShopLogic.close_shop_permanently(username, shop_id)
