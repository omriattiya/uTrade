
from ServiceLayer.services import users,search,items, cart
from django.urls import path

users_urlpatterns = [
    path('users/add_user/', users.add_user),
    path('users/remove_user/', users.remove_user),
    path('users/edit_user/', users.edit_user),
]

search_urlpatterns = [
    path('search/item/', search.search_item)
]

items_urlpatterns = [
    path('items/add_item',items.add_item)
]

cart_urlpatterns = [
    path('cart/add', cart.add_item)
]
urlpatterns = users_urlpatterns + search_urlpatterns + items_urlpatterns + cart_urlpatterns# add more here using '+'
