from django.urls import path

from ServiceLayer.services.LogicServices import SearchService, ItemsService, ShopsService, MessagesService, \
    ShoppingService, AuctionService, LotteryService, UsersService
from ServiceLayer.services.PresentationServices import Home, Profile, Shop, Messages, Item

users_urlpatterns = [
    path('users/register/', UsersService.register),
    path('users/remove_user/', UsersService.remove_user),
    path('users/edit_password/', UsersService.edit_password),
    path('users/login/', UsersService.login),
    path('users/logout/', UsersService.logout),

    path('users/owner/add_owner/', UsersService.add_owner),
    path('users/owner/add_manager/', UsersService.add_manager),
    path('users/owner/remove_manager/', UsersService.remove_manager),
    path('users/owner/update_permissions/', UsersService.update_permissions),
    path('users/owner/close_shop/', UsersService.close_shop),
    path('users/owner/re_open_shop/', UsersService.re_open_shop),
    path('users/owner/modify_notifications/', UsersService.modify_notifications),
    path('users/add_visible_discount', UsersService.add_visible_discount),
    path('users/add_invisible_discount', UsersService.add_invisible_discount),
    path('users/get_visible_discount', UsersService.get_visible_discount),
    path('users/get_invisible_discount', UsersService.get_invisible_discount),
    path('users/get_purchase_history/', UsersService.get_purchase_history),
]

search_urlpatterns = [
    path('search/item/', SearchService.search_item),
    path('search/shop/', SearchService.search_shop),
    path('search/itemInShop/', SearchService.search_item_in_shop),
    path('search/itemsInShop/', SearchService.search_items_in_shop),
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
    path('shops/get_purchase_history/', ShopsService.search_shop_purchase_history),
    path('shops/close_shop_permanently/', ShopsService.close_shop_permanently),
]

system_manager_urlpatterns = [
    path('sys_manager/get_all_purchased_items', ItemsService.get_all_purchased_items),
    path('sys_manager/add_system_manager', UsersService.add_system_manager),
]

messages_urlpatterns = [
    path('messages/send_message/', MessagesService.send_message),
    path('messages/send_message_from_shop/', MessagesService.send_message_from_shop),
    path('messages/get_all_messages/', MessagesService.get_all_messages),
    path('messages/get_all_shop_messages/', MessagesService.get_all_shop_messages)
]

shoppingcart_urlpatterns = [
    path('shopping_cart/add_item_shopping_cart', ShoppingService.add_item_shopping_cart),
    path('shopping_cart/remove_item_shopping_cart/', ShoppingService.remove_item_shopping_cart),
    path('shopping_cart/update_item_shopping_cart/', ShoppingService.update_item_shopping_cart),
    path('shopping_cart/update_code_shopping_cart/', ShoppingService.update_code_shopping_cart),
    path('shopping_cart/get_cart_items/', ShoppingService.get_cart_items),
    path('shopping-cart/pay_all/', ShoppingService.pay_all),
    path('shopping-cart/delivery/', ShoppingService.deliver)
]

lottery_urlpatterns = [
    path('lottery/add_lottery_item_to_shop', LotteryService.add_lottery_item_to_shop)
]

auction_urlpatterns = [
    path('auction/add_auction_to_shop', AuctionService.bid_on_item),
    path('auction/bid_on_item', AuctionService.bid_on_item)
]

home_page_urlpatterns = [
    path('home/', Home.get_home),
    path('home/register/', Home.get_register),
    path('home/messages/', Messages.get_messages)
]

private_area_urlpatterns = [
    path('my/account/', Profile.get_account),
    path('my/shops/', Profile.get_shops),
    path('my/shops/manager/', Profile.get_managers),
    path('my/orders/', Profile.get_orders),
    path('my/orders/order/', Profile.get_order)
]

shop_page_urlpatterns = [
    path('shop/', Shop.get_shop),
    path('shop/reviews/', Shop.get_reviews),
    path('shop/messages/', Messages.get_shop_messages),
    path('shop/get_managers/', Shop.get_shop_managers),
    path('shop/get_owners/', Shop.get_shop_owner),
    path('shop/owner/items/', Shop.get_shop_to_owner),
    path('shop/owner/items/edit_item/', ItemsService.edit_shop_item),
    path('shop/owner/items/remove_item/', ItemsService.remove_item_from_shop),
    path('shop/owner/purchase_history/', Shop.watch_purchase_history)
]

item_page_urlpatterns = [
    path('item/', Item.get_item),
    path('item/reviews/', Item.get_reviews)
]

system_urlpatterns = [
    path('system/shops/', Profile.get_system_shops),
    path('system/users/', Profile.get_system_users),
    path('system/history/', Profile.get_system_history)
]

urlpatterns = users_urlpatterns + \
              search_urlpatterns + \
              items_urlpatterns + \
              shops_urlpatterns + \
              system_manager_urlpatterns + \
              messages_urlpatterns + \
              shoppingcart_urlpatterns + \
              lottery_urlpatterns + \
              auction_urlpatterns + \
              home_page_urlpatterns + \
              private_area_urlpatterns + \
              shop_page_urlpatterns + \
              item_page_urlpatterns + \
              system_urlpatterns  # add more here using '+'
