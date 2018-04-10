from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from DomainLayer import ItemsLogic
from SharedClasses.Item import Item

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('id')
        item_name = request.POST.get('name')
        item_category = request.POST.get('category')
        item_keywords = request.POST.get('keyWords')
        item_rank = request.POST.get('rank')
        item_price = request.POST.get('price')
        item_quantity = request.POST.get('quantity')
        shop_id = request.POST.get('shop_id')
        item = Item(item_id, shop_id, item_name, item_category, item_keywords, item_rank, item_price, item_quantity)
        ItemsLogic.add_item_to_shop(item, shop_id)

@csrf_exempt
def remove_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('item_id')
        ItemsLogic.remove_item_from_shop(item_id)


@csrf_exempt
def add_review_on_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        writer_id = request.POST.get('writer_id')
        item_id = request.POST.get('item_id')
        description = request.POST.get('description')
        rank = request.POST.get('rank')
        ItemsLogic.add_review_on_item(writer_id, item_id, description, rank)


@csrf_exempt
def edit_item(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        item_id = request.POST.get('item_id')
        field_name = request.POST.get('field_name')
        new_value = request.POST.get('new_value')
        status = ItemsLogic.edit_item(username,item_id,field_name,new_value)
        if status:
            return HttpResponse('item edited successfully')
        else:
            return HttpResponse('failed')
