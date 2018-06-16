from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import LotteryLogic, LoggerLogic
from DomainLayer.LoggerLogic import MESSAGE_SQL_INJECTION
from SharedClasses.Item import Item


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
        item = Item(None, shop_name, item_name, item_category, item_keywords, 0, 1, 'prize')
        ticket = Item(None, shop_name, ticket_name, item_category, item_keywords, ticket_price, 1, 'ticket')
        username = request.POST.get('username')

        event = "ADD LOTTERY ITEM"
        suspect_sql_injection = False
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(item_name, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(item_category, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(item_keywords, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(item_price, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(ticket_name, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(ticket_price, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(shop_name, event)
        suspect_sql_injection = suspect_sql_injection and LoggerLogic.identify_sql_injection(username, event)

        if suspect_sql_injection:
            return HttpResponse(MESSAGE_SQL_INJECTION)

        LotteryLogic.add_lottery_and_items(item, ticket, item_price, final_date, username)
