from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ItemsLogic,LotteryLogic
from SharedClasses.Item import Item
from SharedClasses.Lottery import Lottery


@csrf_exempt
def add_lottery_item_to_shop(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_category = request.POST.get('item_category')
        item_keywords = request.POST.get('item_keyWords')
        item_price = request.POST.get('item_price')
        ticket_name = request.POST.get('ticket_name')
        ticket_price = request.POST.get('ticket_price')
        shop_name = request.POST.get('item_shop_name')
        final_date = request.POST.get('final_date')
        item = Item(None, shop_name, item_name, item_category, item_keywords, 0, 1)
        ticket = Item(None, shop_name, ticket_name, item_category, item_keywords, ticket_price, 1)
        username = request.POST.get('username')
        LotteryLogic.add_lottery_and_items(item, ticket, item_price, final_date, username)

