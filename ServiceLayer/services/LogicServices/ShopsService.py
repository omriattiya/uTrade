from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from DomainLayer import ItemsLogic, UsersLogic, LoggerLogic
from DomainLayer import ShopLogic, DiscountLogic
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.InvisibleDiscount import InvisibleDiscount
from SharedClasses.InvisibleDiscountCategory import InvisibleDiscountCategory
from SharedClasses.Shop import Shop
from SharedClasses.ShopReview import ShopReview
from SharedClasses.VisibleDiscount import VisibleDiscount
from SharedClasses.VisibleDiscountCategory import VisibleDiscountCategory


@csrf_exempt
def create_shop(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        shop_name = request.POST.get('name')
        shop_status = request.POST.get('status')

        event = "ADD SHOP"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event) or suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_status, event) or suspect_sql_injection

        if suspect_sql_injection or shop_name == '':
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is None:
            login = request.POST.get('login_hash')
        if login is None:
            return HttpResponse('FAILED: You are not logged in')
        username = Consumer.loggedInUsers.get(login)
        if username is None:
            return HttpResponse('FAILED: You are not logged in')

        shop = Shop(shop_name, shop_status)
        return HttpResponse(ShopLogic.create_shop(shop, username))


@csrf_exempt
def remove_item(request):
    if request.method == 'POST':
        # return HttpResponse('item added')
        item_id = request.POST.get('item_id')
        username = request.POST.get('username')
        ItemsLogic.remove_item_from_shop(item_id, username)


@csrf_exempt
def add_review_on_shop(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        description = request.POST.get('description')
        rank = int(request.POST.get('rank'))

        event = "ADD REVIEW ON SHOP"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event) or suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(description, event) or suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        login = request.COOKIES.get('login_hash')
        if login is not None:
            writer_id = Consumer.loggedInUsers.get(login)
            shop_review = ShopReview(writer_id, description, rank, shop_name)
            old_review = ShopLogic.get_shop_review_with_writer(shop_name, writer_id)
            if old_review is not False:
                return HttpResponse('has reviews')
            if ShopLogic.add_review_on_shop(shop_review):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def close_shop_permanently(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if ShopLogic.close_shop_permanently(username, shop_name):
                return HttpResponse('success')
        return HttpResponse('fail')


@csrf_exempt
def add_discount(request):
    global result
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name')
        percent = int(request.POST.get('percent'))
        kind = request.POST.get('kind')

        event = "ADD DISCOUNT"
        suspect_sql_injection = False
        suspect_sql_injection = LoggerLogic.identify_sql_injection(shop_name, event) or suspect_sql_injection
        suspect_sql_injection = LoggerLogic.identify_sql_injection(kind, event) or suspect_sql_injection

        if suspect_sql_injection:
            return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('duration')
        end_date = end_date.split('-')
        end_date = end_date[0] + '-' + end_date[2] + '-' + end_date[1]
        start_date = start_date.split('-')
        start_date = start_date[0] + '-' + start_date[2] + '-' + start_date[1]

        if shop_name is None or ShopLogic.search_shop(shop_name) is False:
            return HttpResponse('invalid shop')
        login = request.COOKIES.get('login_hash')
        username = None
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is None:
                return HttpResponse('user not logged in')
        if not UsersLogic.is_owner_of_shop(username, shop_name):
            if UsersLogic.is_manager_of_shop(username, shop_name):
                manager = UsersLogic.get_manager(username, shop_name)
                if manager.discount_permission is not 1:  # no permission
                    return HttpResponse('no permission to add discount')
            else:
                return HttpResponse('not owner or manager in this shop')  # not manager not owner

        if kind == "visible_item":
            item_id = request.POST.get('item_id')

            if LoggerLogic.identify_sql_injection(item_id, event):
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            item = ItemsLogic.get_item_without_lottery(item_id)
            if item is False or item.shop_name != shop_name:
                return HttpResponse("item with id=" + item_id + " doesnt exist in this shop or a ticket")
            discount = VisibleDiscount(item_id, shop_name, percent, start_date, end_date)
            result = DiscountLogic.add_visible_discount(discount, username)
        elif kind == "invisible_item":
            item_id = request.POST.get('item_id')
            code = request.POST.get('code')

            suspect_sql_injection = False
            suspect_sql_injection = LoggerLogic.identify_sql_injection(item_id, event) or suspect_sql_injection
            suspect_sql_injection = LoggerLogic.identify_sql_injection(code, event) or suspect_sql_injection

            if suspect_sql_injection:
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            item = ItemsLogic.get_item_without_lottery(item_id)
            if item is False or item.shop_name != shop_name:
                return HttpResponse("item with id=" + item_id + " doesnt exist in this shop or a ticket")

            discount = InvisibleDiscount(code, item_id, shop_name, percent, start_date, end_date)
            result = DiscountLogic.add_invisible_discount(discount, username)
        elif kind == "visible_category":
            category = request.POST.get('category')

            if LoggerLogic.identify_sql_injection(category, event):
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            discount = VisibleDiscountCategory(category, shop_name, percent, start_date, end_date)
            result = DiscountLogic.add_visible_discount_category(discount, username)
        elif kind == "invisible_category":
            category = request.POST.get('category')
            code = request.POST.get('code')

            suspect_sql_injection = False
            suspect_sql_injection = LoggerLogic.identify_sql_injection(category, event) or suspect_sql_injection
            suspect_sql_injection = LoggerLogic.identify_sql_injection(code, event) or suspect_sql_injection

            if suspect_sql_injection:
                return HttpResponse(LoggerLogic.MESSAGE_SQL_INJECTION)

            discount = InvisibleDiscountCategory(code, category, shop_name, percent, start_date, end_date)
            result = DiscountLogic.add_invisible_discount_category(discount, username)

        if result:
            return HttpResponse('success')
        else:
            return HttpResponse('discount already exist for this item/category!')
    else:
        return HttpResponse('FAIL: not post request')


@csrf_exempt
def delete_discount(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('item_id'))
        from_date = request.POST.get('from_date')
        shop_name = request.POST.get('shop_name')
        category = request.POST.get('category')
        type = int(request.POST.get('type'))
        code = request.POST.get('code')

        result_delete = False
        if type == 1:
            result_delete = DiscountLogic.delete_visible_item_discount(item_id, shop_name, from_date)
        if type == 2:
            result_delete = DiscountLogic.delete_visible_category_discount(category, shop_name, from_date)
        if type == 3:
            result_delete = DiscountLogic.delete_invisible_item_discount(item_id, shop_name, from_date, code)
        if type == 4:
            result_delete = DiscountLogic.delete_invisible_category_discount(category, shop_name, from_date, code)

        if result_delete is not False:
            return HttpResponse('success')
        return HttpResponse('TYPE DOES NOT EXIST')
