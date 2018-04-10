from ServiceLayer.services import users, search, items, shops, customer, messages, shoppingcart
from django.urls import path

users_urlpatterns = [
    path('users/register/', users.register),
    path('users/remove_user/', users.remove_user),
    path('users/edit_profile/', users.edit_profile),
    path('users/login/', users.login),

    path('users/owner/add_owner', users.add_owner),
    path('users/owner/add_manager', users.add_manager),
    path('users/owner/close_shop', users.close_shop),
    path('users/owner/re_open_shop', users.re_open_shop),
    path('users/owner/modify_notifications', users.modify_notifications),
]

search_urlpatterns = [
    path('search/item/', search.search_item),
    path('search/shop/', search.search_shop),
    path('search/itemsInShop/', search.search_item_in_shop),
]

items_urlpatterns = [
    path('items/add_item_to_shop/', items.add_item_to_shop),
    path('items/add_item_shopping_cartto_shop/', items.add_item_to_shop),
    path('items/remove_item_from_shop/', items.remove_item_from_shop),
    path('items/add_review_on_item/', items.add_review_on_item),
    path('items/edit_shop_item', items.edit_shop_item)
]

shops_urlpatterns = [
    path('shops/create_shop/', shops.create_shop),
    path('shops/add_review_on_shop/', shops.add_review_on_shop),
    path('shops/get_purchase_history', shops.get_shop_purchase_history)
]

customer_urlpatterns = [
    path('customer/get_purchase_history/', customer.get_purchase_history),
]

messages_urlpatterns = [
    path('messages/send_message/', messages.send_message),
    path('messages/send_message_from_shop', messages.send_message_from_shop),
    path('messages/get_all_messages/', messages.get_all_messages),
    path('messages/get_all_shop_messages', messages.get_all_shop_messages)
]

shoppingcart_urlpatterns = [
    path('shoppingcart/remove_item_shopping_cart/', shoppingcart.remove_item_shopping_cart),
    path('shoppingcart/browse_shopping_cart/', shoppingcart.browse_shopping_cart),
    path('shoppingcart/add', shoppingcart.add_item)
]

urlpatterns = users_urlpatterns + \
              search_urlpatterns + \
              items_urlpatterns + \
              shops_urlpatterns + \
              customer_urlpatterns + \
              messages_urlpatterns + \
              shoppingcart_urlpatterns  # add more here using '+'
