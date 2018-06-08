import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DatabaseLayer import Lotteries, ReviewsOnItems
from DomainLayer import ItemsLogic
from DomainLayer.DiscountLogic import get_visible_discount, get_invisible_discount
from DomainLayer import ShoppingLogic
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar

shop_not_exist = 'item does not exist'
not_get_request = 'not a get request'
is_used = False


def get_item(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item = ItemsLogic.get_item(item_id)
        if item is not False:
            # product = ""
            # product += loader.render_to_string('component/item.html',
            #                                   {'name': item.name, 'price': item.price, 'url': item.url}, None,
            #                                  None)
            right1 = "Percentage"
            policy_or_percentage = "Immediately"
            right2 = "Start Date"
            deadline_or_start_date = "None"
            right3 = "End Time"
            real_end_time_or_end_date = "None"
            headline = "Purchase Policy"
            lottery = Lotteries.get_lottery(item_id)
            quantity_icon = 'icon-inventory.png'
            if lottery is not False:
                right1 = "Policy"
                policy_or_percentage = "Lottery"
                print(lottery.final_date)
                right2 = "Deadline"
                deadline_or_start_date = lottery.final_date
                right3 = "Actual Rnd Time"
                if lottery.real_end_date is not None:
                    real_end_time_or_end_date = lottery.real_end_date
                else: real_end_time_or_end_date = "---------"
                quantity_icon = 'tickets-icon.png'
            else:
                headline = "Discount on Product"
                discount = get_visible_discount(item.id, item.shop_name)
                if discount is not False:
                    deadline_or_start_date  = discount.from_date
                    policy_or_percentage = discount.percentage
                    real_end_time_or_end_date = discount.end_date

            login = request.COOKIES.get('login_hash')
            guest = request.COOKIES.get('guest_hash')
            context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
            item_rank = item.item_rating
            if item_rank is False:
                item_rank = "-----"
            else:
                item_rank = str(item_rank)
            context.update({'item_id': item.id,
                       'item_name': item.name,
                       'shop_name': item.shop_name,
                       'category': item.category,
                       'keyWords': item.keyWords,
                       'price': item.price,
                       'quantity': item.quantity,
                       'kind': item.kind,
                       'item_rank': item_rank,
                       'url': item.url,
                       'policy_or_percentage': policy_or_percentage,
                        'headline': headline,
                       'deadline_or_start_date': deadline_or_start_date,
                       'real_end_time_or_end_date': real_end_time_or_end_date,
                        'right1': right1,
                        'right2': right2,
                        'right3': right3,
                        'quantity_icon': quantity_icon})
            return render(request, 'detail.html', context=context)
        else:
            return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)


def get_reviews(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item = ItemsLogic.get_item(item_id)
        if item is not False:
            reviews = ItemsLogic.get_all_reviews_on_item(item.id)
            string_reviews = ""
            for review in reviews:
                string_reviews += loader.render_to_string(
                    'component/../../../PresentationLayer/templates/components/review.html',
                    {'writer_name': review.writerId, 'rank': review.rank, 'description': review.description}, None, None)
            login = request.COOKIES.get('login_hash')
            guest = request.COOKIES.get('guest_hash')
            context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
            context.update({'item_name': item.name,'shop_name': item.shop_name, 'reviews': string_reviews})
            return render(request, 'item_reviews.html', context=context)
        return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)

