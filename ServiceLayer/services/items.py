from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        return HttpResponse('item added')
