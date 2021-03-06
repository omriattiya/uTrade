from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from DomainLayer import ShoppingLogic, MessagingLogic, UsersLogic
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.PresentationServices import Topbar_Navbar


def get_messages(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        content = request.GET.get('content')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                # html of a logged in user
                messages_html = ""
                if content == 'received':
                    if UsersLogic.is_system_manager(username):
                        messages = MessagingLogic.get_received_system_messages()
                    else:
                        messages = MessagingLogic.get_all_messages(username)
                    for message in messages:
                        messages_html += loader.render_to_string('components/Message.html', context={
                            'id': message.message_id,
                            'from': message.from_username,
                            'to': message.to_username,
                            'content': message.content
                        })
                    received_on = "class=active"
                    sent_on = ""
                elif content == 'sent':
                    if UsersLogic.is_system_manager(username):
                        messages = MessagingLogic.get_sent_system_messages()
                    else:
                        messages = MessagingLogic.get_all_sent_messages(username)
                    for message in messages:
                        messages_html += loader.render_to_string('components/Message.html', context={
                            'id': message.message_id,
                            'from': message.from_username,
                            'to': message.to_username,
                            'content': message.content})
                    received_on = ""
                    sent_on = "class=active"
                else:
                    return HttpResponse('You are not logged in!')
                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'messages': messages_html, 'received_on': received_on, 'sent_on': sent_on})
                return render(request, 'messages.html', context=context)

        return HttpResponse('You are not logged in!')


def get_shop_messages(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        content = request.GET.get('content')
        shop_name = request.GET.get('shop_name')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                messages_html = ""
                if content == 'received':
                    messages = MessagingLogic.get_all_shop_messages(username, shop_name)
                    if messages is not False:
                        for message in messages:
                            messages_html += loader.render_to_string('components/Message.html', context={
                                'id': message.message_id,
                                'from': message.from_username,
                                'to': message.to_username,
                                'content': message.content
                            })
                        received_on = "class=active"
                        sent_on = ""
                    else:
                        return HttpResponse('fail')
                elif content == 'sent':
                    messages = MessagingLogic.get_all_sent_shop_messages(username, shop_name)
                    if messages is not False:
                        for message in messages:
                            messages_html += loader.render_to_string('components/Message.html', context={
                                'id': message.message_id,
                                'from': message.from_username,
                                'to': message.to_username,
                                'content': message.content})
                        received_on = ""
                        sent_on = "class=active"
                    else:
                        return HttpResponse('fail')
                else:
                    return HttpResponse('You are not logged in!')
                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'messages': messages_html, 'received_on': received_on, 'sent_on': sent_on, 'shop_name': shop_name})
                return render(request, 'shop-messages.html', context=context)

        return HttpResponse('You are not logged in!')


def get_alerts(request):
    if request.method == 'GET':
        login = request.COOKIES.get('login_hash')
        if login is not None:
            username = Consumer.loggedInUsers.get(login)
            if username is not None:
                alert_box = Consumer.user_alerts_box.get(username)
                alerts_html=""
                if alert_box is not None:
                    for alert in alert_box:
                        alerts_html += "<tr> <td>"+alert.getContent()+"</td></tr>"

                context = {'topbar': Topbar_Navbar.get_top_bar(login), 'navbar': Topbar_Navbar.get_nav_bar(login, None)}
                context.update({'alerts': alerts_html})
                return render(request, 'alerts-page.html', context=context)
        return HttpResponse('You are not logged in')