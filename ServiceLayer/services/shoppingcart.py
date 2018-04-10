from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingCart


def remove_item_from_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        item_id = request.GET.get('itemId')
        ShoppingCart.remove_item_from_cart(username, item_id)


def remove_item_from_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        ShoppingCart.browse_cart(username)
