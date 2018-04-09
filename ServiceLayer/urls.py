
from ServiceLayer.services import users,search,items
from django.urls import path

users_urlpatterns = [
    path('users/add_user/', users.add_user),
    path('users/remove_user/', users.remove_user),
    path('users/edit_user/', users.edit_user),
]

search_urlpatterns = [
    path('search/item/', search.search_item),
    path('search/shop/', search.search_shop),
    path('search/itemsInShop/', search.search_item_in_shop)
]

items_urlpatterns = [
    path('items/add_item', items.add_item)
]

urlpatterns = users_urlpatterns + search_urlpatterns + items_urlpatterns# add more here using '+'
