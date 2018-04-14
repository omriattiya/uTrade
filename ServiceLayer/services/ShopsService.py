from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ItemsLogic
from DomainLayer import ShopLogic
from SharedClasses.Shop import Shop
from SharedClasses.ShopReview import ShopReview


@csrf_exempt
def create_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        shop_name = request.POST.get('name')
        shop_status = request.POST.get('status')
        username = request.POST.get('username')
        shop = Shop(shop_name, shop_status)
        ShopLogic.create_shop(shop, username)


@csrf_exempt
def remove_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('item_id')
        username = request.POST.get('username')
        ItemsLogic.remove_item_from_shop(item_id,username)


@csrf_exempt
def add_review_on_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        writer_id = request.POST.get('writer_id')
        shop_name = request.POST.get('shop_name')
        description = request.POST.get('description')
        rank = request.POST.get('rank')
        shop_review = ShopReview(writer_id,description,rank,shop_name)
        ShopLogic.add_review_on_shop(shop_review)


def search_shop_purchase_history(request):
    if request.method == 'GET':
        return HttpResponse('no GUI yet')


@csrf_exempt
def close_shop_permanently(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        shop_name = request.POST.get('shop_name')
        # return HttpResponse('no GUI yet')
        ShopLogic.close_shop_permanently(username, shop_name)
