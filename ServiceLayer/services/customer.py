from DomainLayer import Customer


def get_purchase_history(request):
    if request.method == 'GET':
        # return HttpResponse('item added')
        user_id = request.GET.get('user_id')
        Customer.get_purchase_history(user_id)
