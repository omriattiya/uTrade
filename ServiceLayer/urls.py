from ServiceLayer.services import UsersService, SearchService, ItemsService, ShopsService, MessagesService, ShoppingService
from django.urls import path

users_urlpatterns = [
    path('users/register/', UsersService.register),
    path('users/remove_user/', UsersService.remove_user),
    path('users/edit_profile/', UsersService.edit_profile),
    path('users/login/', UsersService.login),

    path('users/owner/add_owner', UsersService.add_owner),
    path('users/owner/add_manager', UsersService.add_manager),
    path('users/owner/close_shop', UsersService.close_shop),
    path('users/owner/re_open_shop', UsersService.re_open_shop),
    path('users/owner/modify_notifications', UsersService.modify_notifications),
    path('users/add_visible_discount', UsersService.add_visible_discount),
    path('users/add_invisible_discount', UsersService.add_invisible_discount),
    path('users/get_visible_discount', UsersService.get_visible_discount),
    path('users/get_invisible_discount', UsersService.get_invisible_discount),
    path('users/get_purchase_history/', UsersService.get_purchase_history),
]

search_urlpatterns = [
    path('search/item/', SearchService.search_item),
    path('search/shop/', SearchService.search_shop),
    path('search/itemsInShop/', SearchService.search_item_in_shop),
]

items_urlpatterns = [
    path('items/add_item_to_shop/', ItemsService.add_item_to_shop),
    path('items/remove_item_from_shop/', ItemsService.remove_item_from_shop),
    path('items/add_review_on_item/', ItemsService.add_review_on_item),
    path('items/edit_shop_item', ItemsService.edit_shop_item)
]

shops_urlpatterns = [
    path('shops/create_shop/', ShopsService.create_shop),
    path('shops/add_review_on_shop/', ShopsService.add_review_on_shop),
    path('shops/get_purchase_history', ShopsService.search_shop_purchase_history),
    path('shops/close_shop_permanently', ShopsService.close_shop_permanently),
]

system_manager_urlpatterns = [
    path('sys_manager/get_all_purchased_items', ItemsService.get_all_purchased_items),
    path('sys_manager/add_system_manager', UsersService.add_system_manager),
]

messages_urlpatterns = [
    path('messages/send_message/', MessagesService.send_message),
    path('messages/send_message_from_shop', MessagesService.send_message_from_shop),
    path('messages/get_all_messages/', MessagesService.get_all_messages),
    path('messages/get_all_shop_messages', MessagesService.get_all_shop_messages)
]

shoppingcart_urlpatterns = [
    path('shopping_cart/add_item_shopping_cart', ShoppingService.add_item_shopping_cart),
    path('shopping_cart/remove_item_shopping_cart/', ShoppingService.remove_item_shopping_cart),
    path('shopping_cart/update_item_shopping_cart/', ShoppingService.update_item_shopping_cart),
    path('shopping_cart/update_code_shopping_cart/', ShoppingService.update_code_shopping_cart),
    path('shopping_cart/get_cart_items/', ShoppingService.get_cart_items),
    path('shopping-cart/pay_all', ShoppingService.pay_all)

]

urlpatterns = users_urlpatterns + \
              search_urlpatterns + \
              items_urlpatterns + \
              shops_urlpatterns + \
              system_manager_urlpatterns + \
              messages_urlpatterns + \
              shoppingcart_urlpatterns  # add more here using '+'
