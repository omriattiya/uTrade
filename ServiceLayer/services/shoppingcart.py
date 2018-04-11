from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingLogic


def remove_item_shopping_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        item_id = request.GET.get('itemId')
        ShoppingLogic.remove_item_shopping_cart(username, item_id)


def browse_shopping_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        ShoppingLogic.browse_shopping_cart(username)


@csrf_exempt
def add_item_shopping_cart(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        ShoppingLogic.add_item_shopping_cart(user_id, item_id, quantity)
        return HttpResponse('item added to cart')
