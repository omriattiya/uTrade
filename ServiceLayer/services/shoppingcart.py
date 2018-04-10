from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DomainLayer import ShoppingCart


def remove_item_from_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        item_id = request.GET.get('itemId')
        ShoppingCart.remove_item_from_cart(username, item_id)


def browse_cart(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        ShoppingCart.browse_cart(username)


@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        ShoppingCart.add_item(user_id, item_id, quantity)
        return HttpResponse('item added to cart')
