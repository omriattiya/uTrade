from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DatabaseLayer import Lotteries
from DomainLayer import ItemsLogic
from DomainLayer.DiscountLogic import get_visible_discount, get_visible_discount_category
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
            policy_or_percentage = "0"
            item_percentage = "0"
            right2 = "Start Date"
            deadline_or_start_date = "None"
            item_start_date = "None"
            item_end_date = "None"
            right3 = "End Time"
            real_end_time_or_end_date = "None"
            headline = "Purchase Policy"
            price = item.price
            former_price = ""
            lottery = Lotteries.get_lottery(item_id)
            invisible = ""
            header_of_table = "Category Discount"
            lottery_margin_left = 0
            quantity_icon = 'icon-inventory.png'
            if lottery is not False:
                right1 = "Policy"
                policy_or_percentage = "Lottery"
                print(lottery.final_date)
                right2 = "Deadline"
                deadline_or_start_date = lottery.final_date
                right3 = "Actual End Time"
                invisible = "display: none;"
                header_of_table = "Additional details you should know before purchase"
                lottery_margin_left = 30
                if lottery.real_end_date is not None:
                    real_end_time_or_end_date = lottery.real_end_date
                else:
                    real_end_time_or_end_date = "---------"
                quantity_icon = 'tickets-icon.png'
            else:
                headline = "Discounts on Product"
                discount = get_visible_discount(item.id, item.shop_name)
                if discount is not False:
                    item_start_date = discount.from_date
                    item_percentage = str(discount.percentage) + "%"
                    item_end_date = discount.end_date
                    former_price = "$" + str(item.price)
                    price = price*(1 - (discount.percentage / 100))
                discount = get_visible_discount_category(item.category, item.shop_name)
                if discount is not False:
                    deadline_or_start_date = discount.from_date
                    policy_or_percentage = str(discount.percentage) + "%"
                    real_end_time_or_end_date = discount.end_date
                    former_price = "$" + str(item.price)
                    price = price * (1 - (discount.percentage / 100))
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
                            'price': round(price, 2),
                            'former_price': former_price,
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
                            'header_of_table': header_of_table,
                            'invisible': invisible,
                            'lottery_margin_left': lottery_margin_left,
                            'item_percentage': item_percentage,
                            'item_start_date': item_start_date,
                            'item_end_date': item_end_date,
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
                    {'writer_name': review.writerId, 'rank': review.rank, 'description': review.description}, None,
                    None)
            login = request.COOKIES.get('login_hash')
            guest = request.COOKIES.get('guest_hash')
            context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, guest)}
            context.update({'item_name': item.name, 'shop_name': item.shop_name, 'reviews': string_reviews})
            return render(request, 'item_reviews.html', context=context)
        return HttpResponse(shop_not_exist)
    return HttpResponse(not_get_request)
