from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import MessagingLogic


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message_from = request.POST.get('from')
        message_to = request.POST.get('to')
        content = request.POST.get('content')
        MessagingLogic.send_message(message_from, message_to, content)


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
        message = request.POST.get('message')
        shop_name = request.POST.get('shop_name')
        to = request.POST.get('to')
        if MessagingLogic.send_message_from_shop(username,message,shop_name,to):
            return HttpResponse('sent successfully')
    return HttpResponse('failed')