from django.views.decorators.csrf import csrf_exempt
from DomainLayer import MessagingLogic


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        message_from = request.POST.get('from')
        message_to = request.POST.get('to')
        content = request.POST.get('content')
        MessagingLogic.send_message(message_from, message_to, content)


def get_all_messages(request):
    if request.method == 'GET':
        # return HttpResponse('item added')
        id = request.GET.get('id')
        MessagingLogic.get_all_messages(id)
