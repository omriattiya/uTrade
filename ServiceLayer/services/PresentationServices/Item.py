import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DatabaseLayer import Lotteries, Auctions
from DomainLayer import ItemsLogic
from ServiceLayer import Consumer

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
            policy = "Immediately"
            deadline = "------"
            real_end_time = "------"
            lottery = Lotteries.get_lottery(item_id)
            if lottery is not False:
                policy = "Lottery"
                deadline = datetime.datetime.fromtimestamp(lottery.final_date/1000).strftime('%c')
                if lottery.real_end_date is not None:
                    real_end_time = datetime.datetime.fromtimestamp(lottery.real_end_date/1000).strftime('%c')
            else:
                auction = Auctions.get_auction(item_id)
                if auction is not False:
                    policy = "Auction"
                    deadline = datetime.datetime.fromtimestamp(auction.end_date/1000).strftime('%c')
            login = request.COOKIES.get('login_hash')
            username = "guest"
            if login is not None:
                username = Consumer.loggedInUsers.get(login)
            context = {'item_id': item.id,
                       'item_name': item.name,
                       'shop_name': item.shop_name,
                       'category': item.category,
                       'keyWords': item.keyWords,
                       'price': item.price,
                       'quantity': item.quantity,
                       'kind': item.kind,
                       'url': item.url,
                       'policy': policy,
                       'deadline': deadline,
                       'real_end_time': real_end_time,
                       'username': username}
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
