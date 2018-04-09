from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from DomainLayer import ShoppingCart

@csrf_exempt
def add_item(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        item_id = request.POST.get("item_id")
        quantity = request.POST.get("quantity")
        ShoppingCart.add_item_to_cart(user_id,item_id,quantity)
        return HttpResponse('item added to cart')