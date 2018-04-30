from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from DomainLayer import ItemsLogic
from SharedClasses.Item import Item
from SharedClasses.ItemReview import ItemReview


@csrf_exempt
def add_item_to_shop(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        item_category = request.POST.get('category')
        item_keywords = request.POST.get('keyWords')
        item_price = request.POST.get('price')
        item_quantity = request.POST.get('quantity')
        shop_name = request.POST.get('shop_name')
        item = Item(None, shop_name, item_name, item_category, item_keywords, item_price, item_quantity, 'regular')
        username = request.POST.get('username')
        ItemsLogic.add_item_to_shop(item, username)


@csrf_exempt
def remove_item_from_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('item_id')
        username = request.POST.get('username')
        ItemsLogic.remove_item_from_shop(item_id, username)


@csrf_exempt
def add_review_on_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        writer_name = request.POST.get('writer_name')
        item_id = request.POST.get('item_id')
        description = request.POST.get('description')
        rank = request.POST.get('rank')
        review = ItemReview(writer_name,description,rank,item_id)
        ItemsLogic.add_review_on_item(review)


@csrf_exempt
def edit_shop_item(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        item_id = request.POST.get('item_id')
        field_name = request.POST.get('field_name')
        new_value = request.POST.get('new_value')
        status = ItemsLogic.edit_shop_item(username, item_id, field_name, new_value)
        if status:
            return HttpResponse('item edited successfully')
        else:
            return HttpResponse('failed')


def get_all_purchased_items(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        return ItemsLogic.get_all_purchased_items(username)

