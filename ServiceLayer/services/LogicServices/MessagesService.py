from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import MessagingLogic, LoggerLogic
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.Message import Message


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message_to = request.POST.get('to')
        content = request.POST.get('content')

        event = "SEND MESSAGE"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(message_to, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(content, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            message_from = Consumer.loggedInUsers.get(login)

            message = Message(None, message_from, message_to, content)
            return HttpResponse(MessagingLogic.send_message(message))
        return HttpResponse('FAILED: You are not logged in')


def get_all_messages(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        MessagingLogic.get_all_messages(username)


def get_all_shop_messages(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        shop_name = request.GET.get('shop_name')
        MessagingLogic.get_all_shop_messages(username, shop_name)


@csrf_exempt
def send_message_from_shop(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        from_shop = request.POST.get('from')
        to = request.POST.get('to')

        event = "SEND MESSAGE FROM SHOP"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(content, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(from_shop, event) and suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(to, event) and suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            message = Message(None, from_shop, to, content)
            return HttpResponse(MessagingLogic.send_message_from_shop(username, message))

        return HttpResponse('FAILED: You are not logged in')
