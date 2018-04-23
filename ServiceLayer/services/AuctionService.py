from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from SharedClasses.AuctionBid import AuctionBid
@csrf_exempt
def bid_on_item(request):
    if request.method == 'POST':
        auction_id = request.POST.get("auction_id")
        username = request.POST.get("username")
        price = request.POST.get("price")
        auction_bid = AuctionBid(auction_id,username,price)
        AuctionLogic.add_item_shopping_cart(auction_bid)
        return HttpResponse('item added to cart')
