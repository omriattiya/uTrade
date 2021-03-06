from django.urls import path

from ServiceLayer.services.LogicServices import SearchService, ItemsService, ShopsService, MessagesService, \
    ShoppingService, LotteryService, UsersService, ShoppingPolicyService
from ServiceLayer.services.PresentationServices import Home, Profile, Shop, Messages, Item, ShoppingCart, Policy

users_urlpatterns = [
    path('users/register/', UsersService.register),
    path('users/remove_user/', UsersService.remove_user),
    path('users/edit_password/', UsersService.edit_password),
    path('users/update_details/', UsersService.update_details),
    path('users/login/', UsersService.login),
    path('users/logout/', UsersService.logout),
    path('users/clear_alerts/', UsersService.clear_alerts),

    path('users/owner/add_owner/', UsersService.add_owner),
    path('users/owner/add_manager/', UsersService.add_manager),
    path('users/owner/remove_manager/', UsersService.remove_manager),
    path('users/owner/update_permissions/', UsersService.update_permissions),
    path('users/owner/close_shop/', UsersService.close_shop),
    path('users/owner/re_open_shop/', UsersService.re_open_shop),
    path('users/owner/modify_notifications/', UsersService.modify_notifications),
    path('users/get_visible_discount', UsersService.get_visible_discount),
    path('users/get_invisible_discount', UsersService.get_invisible_discount),
    path('users/get_purchase_history/', UsersService.get_purchase_history),
]

search_urlpatterns = [
    path('search/item/', SearchService.search_item),
    path('search/shop/', Shop.get_shop),
    path('search/itemInShop/', SearchService.search_item_in_shop),
    path('search/itemsInShop/', SearchService.search_items_in_shop),
]

items_urlpatterns = [
    path('items/add_item_to_shop/', ItemsService.add_item_to_shop),
    path('items/remove_item_from_shop/', ItemsService.remove_item_from_shop),
    path('items/add_review_on_item/', ItemsService.add_review_on_item),
    path('items/edit_shop_item/', ItemsService.edit_shop_item),
    path('items/get_id_by_name/',ItemsService.get_id_by_name)
]

shops_urlpatterns = [
    path('shops/create_shop/', ShopsService.create_shop),
    path('shops/add_review_on_shop/', ShopsService.add_review_on_shop),
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
    path('shopping_cart/add_item_shopping_cart/', ShoppingService.add_item_to_cart),
    path('shopping_cart/remove_item_shopping_cart/', ShoppingService.remove_item_shopping_cart),
    path('shopping_cart/update_item_shopping_cart/', ShoppingService.update_item_shopping_cart),
    path('shopping_cart/update_code_shopping_cart/', ShoppingService.update_code_shopping_cart),
    path('shopping_cart/get_cart_items/', ShoppingCart.get_cart_items),
    path('shopping_cart/pay_all/', ShoppingService.pay_all),
    path('shopping_cart/addressing/', ShoppingCart.address),
    path('shopping_cart/review_order/', ShoppingCart.review_order),
    path('shopping_cart/check_empty_cart/', ShoppingService.check_valid_cart),
    path('shopping_cart/receipt/', ShoppingCart.show_receipt)
]

lottery_urlpatterns = [
    path('lottery/add_lottery_item_to_shop', LotteryService.add_lottery_item_to_shop)
]

home_page_urlpatterns = [
    path('home/', Home.get_home),
    path('home/register/', Home.get_register),
    path('home/messages/', Messages.get_messages),
    path('home/alerts/', Messages.get_alerts)
]

private_area_urlpatterns = [
    path('my/account/', Profile.get_account),
    path('my/shops/', Profile.get_shops),
    path('my/shops/manager/', Profile.get_managers),
    path('my/orders/', Profile.get_orders),
    path('my/orders/order/', Profile.get_order),
    path('my/historyappointings/', Profile.get_history_appoitings)
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
    path('shop/owner/items/add_item/', Shop.add_item_to_shop),
    path('shop/owner/items/add_item/post', ItemsService.add_item_to_shop),
    path('shop/owner/purchase_history/', Shop.watch_purchase_history),
    path('shop/owner/add_discount/', Shop.add_discount_page),
    path('shop/owner/add_discount/post', ShopsService.add_discount),
    path('shop/owner/delete_discount/', Shop.delete_discount),
    path('shop/owner/delete_discount/post', ShopsService.delete_discount),

]

item_page_urlpatterns = [
    path('item/', Item.get_item),
    path('item/reviews/', Item.get_reviews)
]

system_urlpatterns = [
    path('system/shops/', Profile.get_system_shops),
    path('system/users/', Profile.get_system_users),
    path('system/history/', Profile.get_system_history),
    path('system/logger/', Profile.get_system_log),
    path('system/logger/event/', Profile.get_system_log_event),
    path('system/logger/error/', Profile.get_system_log_error),
    path('system/logger/login/', Profile.get_system_log_login),
    path('system/logger/security/', Profile.get_system_log_security),
    path('system/con_reporting/', Profile.continuous_reporting),
    path('system/con_reporting/login_gap/', Profile.login_gap),
]

policies_urlpatterns = [
    path('policies/shopping/shop/', Policy.getShopShoppingPolicies),
    path('policies/shopping/shop/add/', ShoppingPolicyService.add_shopping_policy_on_shop),
    path('policies/shopping/shop/conditions/', Policy.getShopShoppingPolicyConditions),
    path('policies/shopping/shop/update/', ShoppingPolicyService.update_shopping_policy_on_shop),
    path('system/policies/', Profile.get_system_policies),
    path('system/policies/item/add/', ShoppingPolicyService.add_shopping_policy_on_items),
    path('system/policies/item/update/', ShoppingPolicyService.update_shopping_policy_on_items),
    path('system/policies/item/get/conditions/', Policy.getItemShoppingPolicyConditions),
    path('system/policies/category/add/', ShoppingPolicyService.add_shopping_policy_on_category),
    path('system/policies/category/update/', ShoppingPolicyService.update_shopping_policy_on_category),
    path('system/policies/category/get/conditions/', Policy.getCategoryShoppingPolicyConditions),
    path('system/policies/global/add/', ShoppingPolicyService.add_shopping_policy_on_identity),
    path('system/policies/global/update/', ShoppingPolicyService.update_shopping_policy_on_identity),
    path('system/policies/global/get/conditions/', Policy.getGlobalShoppingPolicyConditions)

]

urlpatterns = users_urlpatterns + \
              search_urlpatterns + \
              items_urlpatterns + \
              shops_urlpatterns + \
              system_manager_urlpatterns + \
              messages_urlpatterns + \
              shoppingcart_urlpatterns + \
              lottery_urlpatterns + \
              home_page_urlpatterns + \
              private_area_urlpatterns + \
              shop_page_urlpatterns + \
              item_page_urlpatterns + \
              system_urlpatterns + \
              policies_urlpatterns  # add more here using '+'
