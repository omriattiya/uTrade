import os
import time
import unittest

from DatabaseLayer import PurchasedItems
from DatabaseLayer.Items import search_item_in_shop, add_item_to_shop
from DatabaseLayer.PurchasedItems import add_purchased_item
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ReviewsOnItems import get_all_reviews_on_item
from DatabaseLayer.Shops import search_shop
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic
from DomainLayer.ItemsLogic import get_all_purchased_items, remove_item_from_shop, edit_shop_item
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.ItemReview import ItemReview
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.StoreManager import StoreManager
from SharedClasses.SystemManager import SystemManager


class ItemsTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        register(RegisteredUser('StoreManager0', '1234567878'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager0', 'My Shop', 0, 0, 0, 0, 0, 0, 0))

    def test_get_all_purchased_items(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user = get_user('ToniToniToniToni')
        user1user1 = get_user('NoniNoni')
        add_system_manager(SystemManager(user.username, user.password))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500)
        add_item_to_shop(item1)
        add_purchased_item(item1.id, 50, 7, item1.price, user1user1.username)
        lst = get_all_purchased_items('ToniToniToniToni')
        self.assertTrue(len(lst) > 0)

    def test_bad_no_itemsget_all_purchased_items(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user = get_user('ToniToniToniToni')
        add_system_manager(SystemManager(user.username, user.password))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500)
        add_item_to_shop(item1)
        lst = get_all_purchased_items('ToniToniToniToni')
        self.assertFalse(len(lst) > 0)

    def test_bad_sysman_get_all_purchased_items(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user1user1 = get_user('NoniNoni')
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500)
        add_item_to_shop(item1)
        add_purchased_item(item1.id, 50, 7, item1.price, user1user1.username)
        self.assertFalse(get_all_purchased_items('ToniToniToniToni'))

    def test_review_on_item(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'YoniYoni')
        PurchasedItems.add_purchased_item(1, time.time(), 5, 10, 'TomerTomer')
        ItemsLogic.add_review_on_item(ItemReview('TomerTomer', 'Good', 10, 1))
        reviews = get_all_reviews_on_item(1)
        self.assertEqual(len(reviews), 1)

    def test_review_on_item_bad(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'YoniYoni')
        ItemsLogic.add_review_on_item(ItemReview('TomerTomer', 'Good', 10, 1))
        reviews = get_all_reviews_on_item(1)
        self.assertEqual(reviews, [])

    def test_review_on_item_bad_writer(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'YoniYoni')
        PurchasedItems.add_purchased_item(1, time.time(), 5, 10, 'TomerTomer')
        ItemsLogic.add_review_on_item(ItemReview('TomerYoni', 'Good', 10, 1))
        self.assertFalse(get_all_reviews_on_item(1))

    def test_add_item_to_shop(self):
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        # condition1 = check_in_stock(item1.id, 100) and check_in_stock(item2.id, 100)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)

    def test_bad_quantity_of_item(self):
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, -5)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, -7)
        status1 = ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        status2 = ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        self.assertFalse(status1)
        self.assertFalse(status2)

    def test_bad_add_item_to_shop(self):
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        item3 = Item(3, 'My Shop', 'tomato', 'vegetables', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        # condition1 = check_in_stock(item1.id, 100) and check_in_stock(item2.id, 100)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)
        self.assertFalse(search_item_in_shop(shop.name, item3.id))

    def test_remove_item_from_shop(self):
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)
        self.assertTrue(remove_item_from_shop(item1.id, 'StoreManager1'))
        self.assertFalse(search_item_in_shop(shop.name, item1.name))

    def test_bad_shopless_item_remove_item_from_shop(self):
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertFalse(remove_item_from_shop(item2.id, 'StoreManager1'))
        self.assertTrue(search_item_in_shop(shop.name, item1.name))

    def test_bad_man_remove_item_from_shop(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertFalse(remove_item_from_shop(item1.id, 'TomerTomer'))
        self.assertTrue(search_item_in_shop(shop.name, item1.name))

    def test_edit_shop_item(self):
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)
        self.assertTrue(edit_shop_item('StoreManager1', item1.id, 'price', 15))
        price = search_item_in_shop(shop.name, item1.name).price
        self.assertEqual(15, price)

    def test_bad_category_edit_shop_item(self):
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)
        self.assertFalse(edit_shop_item('StoreManager1', item1.id, 'mistake', 15))
        price = search_item_in_shop(shop.name, item1.name).price
        self.assertEqual(12, price)

    def test_bad_no_man_edit_shop_item(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)
        self.assertFalse(edit_shop_item('TomerTomer', item1.id, 'price', 15))
        price = search_item_in_shop(shop.name, item1.name).price
        self.assertEqual(12, price)

    def test_bad_premission_edit_shop_item(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        shop = search_shop('My Shop')
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        searched_1 = search_item_in_shop(shop.name, item1.name)
        searched_2 = search_item_in_shop(shop.name, item2.name)
        self.assertEqual(searched_1.id, item1.id)
        self.assertEqual(searched_2.id, item2.id)
        self.assertFalse(edit_shop_item('StoreManager0', item1.id, 'price', 15))
        price = search_item_in_shop(shop.name, item1.name).price
        self.assertEqual(12, price)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()