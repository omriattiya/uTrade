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


def add_to_db():
    is_used = True
    shop_name = 'my_shop'
    username = 'omriatti'
    UsersLogic.register(RegisteredUser(username, '12345678'))
    ShopLogic.create_shop(Shop(shop_name, 'ACTIVE'), username)
    ItemsLogic.add_item_to_shop(Item(1, shop_name, 'tomato', 'fruits', '', 20, 70, 'regular',
                                     'https://cdn.shopify.com/s/files/1/1380/2059/products/Cherry-Tomato_600x600.jpg?v=1480318422'),
                                username)
    ShopLogic.add_review_on_shop(ShopReview(username, "THIS IS AMAZING SHOP I BUT HERE EVERY DAY", 5, shop_name))


def get_shop(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            items = ShopLogic.get_shop_items(shop.name)
            products = ""
            for item in items:
                products += loader.render_to_string('component/item.html',
                                                    {'name': item.name, 'price': item.price, 'url': item.url}, None,
                                                    None)
            context = {'shop_name': shop.name,
                       'shop_status': shop.status,
                       'products': products}
            return render(request, 'shop.html', context=context)
        else:
            return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_reviews(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        shop = ShopLogic.search_shop(shop_name)
        if shop is not False:
            reviews = ShopLogic.get_shop_reviews(shop_name)
            string_reviews = ""
            for review in reviews:
                string_reviews += loader.render_to_string('component/review.html',
                                                          {'writer_name': review.writerId,
                                                           'rank': review.rank,
                                                           'description': review.description}, None, None)
            context = {'shop_name': shop_name, 'reviews': string_reviews}
            return render(request, 'shop_reviews.html', context=context)
        return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)
