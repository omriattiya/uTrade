from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import ShopLogic, UsersLogic, ItemsLogic
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.ShopReview import ShopReview

shop_not_exist = 'shop does not exist'
not_get_request = 'not a get request'
is_used = False


def get_item(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item = ItemsLogic.get_item(item_id)
        if item is not False:
            # product = ""
            # product += loader.render_to_string('component/item.html',
            #                                   {'name': item.name, 'price': item.price, 'url': item.url}, None,
            #                                  None)
            context = {'item_id': item.id,
                       'item_name': item.name,
                       'shop_name': item.shop_name,
                       'category': item.category,
                       'keyWords': item.keyWords,
                       'price': item.price,
                       'quantity': item.quantity,
                       'kind': item.kind}
            return render(request, 'detail.html', context=context)
        else:
            return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_reviews(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item = ItemsLogic.get_item(item_id)
        if item is not False:
            reviews = ItemsLogic.get_all_reviews_on_item(item.id)
            string_reviews = ""
            for review in reviews:
                string_reviews += loader.render_to_string('component/review.html',
                                                          {'writer_name': review.writerId,
                                                           'rank': review.rank,
                                                           'description': review.description}, None, None)
            context = {'item_name': item.name, 'shop_name': item.shop_name, 'reviews': string_reviews}
            return render(request, 'item_reviews.html', context=context)
        return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)
