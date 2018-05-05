from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ItemsLogic, UsersLogic
from ServiceLayer import Consumer
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
        login = request.COOKIES.get('login_hash')
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('fail')

        item_id = request.POST.get('item_id')

        item = ItemsLogic.get_item(item_id)
        if item is False:
            return HttpResponse('fail')
        if not UsersLogic.is_owner_of_shop(username, item.shop_name):
            if UsersLogic.is_manager_of_shop(username, item.shop_name):
                manager = UsersLogic.get_manager(username, item.shop_name)
                if manager.permission_remove_item is not 1:  # no permission
                    return HttpResponse('no permission to remove item')
            else:
                return HttpResponse('fail')  # not manager not owner

        status = ItemsLogic.remove_item_from_shop(item_id, username)
        if status is False:
            return HttpResponse('fail')
        return HttpResponse('success')


@csrf_exempt
def add_review_on_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        description = request.POST.get('description')
        rank = request.POST.get('rank')

        login = request.COOKIES.get('login_hash')
        if login is not None:
            writer_name = Consumer.loggedInUsers.get(login)
            review = ItemReview(writer_name, description, rank, item_id)

            if ItemsLogic.add_review_on_item(review):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def edit_shop_item(request):
    if request.method == 'POST':
        login = request.COOKIES.get('login_hash')
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('fail')
        item_id = request.POST.get('item_id')

        item = ItemsLogic.get_item(item_id)
        if item is False:
            return HttpResponse('fail')
        if not UsersLogic.is_owner_of_shop(username, item.shop_name):
            if UsersLogic.is_manager_of_shop(username, item.shop_name):
                manager = UsersLogic.get_manager(username, item.shop_name)
                if manager.permission_edit_item is not 1:  # no permission
                    return HttpResponse('no permission to edit item')
            else:
                return HttpResponse('fail')  # not manager not owner

        fields = ['quantity', 'category', 'keywords', 'price', 'url']
        new_values = [request.POST.get('item_quantity'),
                      request.POST.get('item_category'),
                      request.POST.get('item_keywords'),
                      request.POST.get('item_price'),
                      request.POST.get('item_url')]
        status = True
        for i in range(0, len(fields)):
            status = ItemsLogic.edit_shop_item(username, item_id, fields[i], new_values[i])
            if status is False:
                return HttpResponse('fail')
        return HttpResponse('success')


def get_all_purchased_items(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        return ItemsLogic.get_all_purchased_items(username)
