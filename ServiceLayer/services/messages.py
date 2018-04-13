from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import MessagingLogic
from SharedClasses.Message import Message

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message_from = request.POST.get('from')
        message_to = request.POST.get('to')
        content = request.POST.get('content')
        message = Message(None,message_from,message_to,content)
        MessagingLogic.send_message(message)


def get_all_messages(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        MessagingLogic.get_all_messages(username)


def get_all_shop_messages(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        shop_name = request.GET.get('shop_name')
        MessagingLogic.get_all_shop_messages(username, shop_name)


def send_message_from_shop(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        content = request.POST.get('content')
        from_shop = request.POST.get('from')
        to = request.POST.get('to')
        message = Message(None,from_shop,to,content)
        if MessagingLogic.send_message_from_shop(username,message):
            return HttpResponse('sent successfully')
    return HttpResponse('failed')