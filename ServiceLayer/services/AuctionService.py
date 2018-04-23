from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from SharedClasses.Auction import Auction
from SharedClasses.AuctionBid import AuctionBid
from DomainLayer import AuctionLogic, ItemsLogic
from SharedClasses.Item import Item


@csrf_exempt
def bid_on_item(request):
    if request.method == 'POST':
        auction_id = request.POST.get("auction_id")
        username = request.POST.get("username")
        price = request.POST.get("price")
        auction_bid = AuctionBid(auction_id, username, price)
        AuctionLogic.bid_on_item(auction_bid)
        return HttpResponse('item bid success')


@csrf_exempt
def add_auction_to_shop(request):
    if request.method == 'POST':
        item_name = request.POST.get('name')
        item_category = request.POST.get('category')
        item_keywords = request.POST.get('keyWords')
        item_price = request.POST.get('price')
        item_quantity = request.POST.get('quantity')
        shop_name = request.POST.get('shop_name')
        end_date = request.POST.get('end_date')
        item = Item(None, shop_name, item_name, item_category, item_keywords, item_price, item_quantity)
        username = request.POST.get('username')
        item_id = ItemsLogic.add_item_to_shop(item, username)
        auction = Auction(item_id, end_date)
        AuctionLogic.add_auction(auction)

