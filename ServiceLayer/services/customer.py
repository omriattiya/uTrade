import DomainLayer.ItemsLogic
from DomainLayer import ItemsLogic


def get_purchase_history(request):
    if request.method == 'GET':
        # return HttpResponse('item added')
        user_id = request.GET.get('user_id')
        DomainLayer.ItemsLogic.get_purchase_history(user_id)
