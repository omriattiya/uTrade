import os
import unittest
import time

from DatabaseLayer.Items import search_item_in_shop
from DatabaseLayer.PurchasedItems import add_purchased_item
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ReviewsOnItems import get_all_reviews_on_item
from DatabaseLayer.Shops import search_shop
from DatabaseLayer.StoreManagers import add_manager
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer import PurchasedItems
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic
from DomainLayer.ItemsLogic import get_all_purchased_items, check_in_stock, remove_item_from_shop, edit_shop_item
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.StoreManager import StoreManager
from SharedClasses.SystemManager import SystemManager
from SharedClasses.PurchasedItem import PurchasedItem

class ItemsTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('Yoni', '12345678'))
        register(RegisteredUser('StoreManager1', '12345678'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'Yoni')
        UsersLogic.add_manager('Yoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1))

    def test_get_all_purchased_items(self):
        register(RegisteredUser('Yoni', '121212'))
        user = get_user('Yoni')
        add_system_manager(SystemManager(user.username, user.password))
        add_purchased_item("banana", 'Yoni')
        lst = get_all_purchased_items('Yoni')
        self.assertTrue(len(lst) > 0)

    def test_review_on_item(self):
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'Tomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'Tomer')
        PurchasedItems.add_purchased_item(1, time.time(), 5, 10, 'Tomer')
        ItemsLogic.add_review_on_item('Tomer', 1, 'Good', 10)
        reviews = get_all_reviews_on_item(1)
        self.assertEqual(len(reviews), 1)

    def test_review_on_item_bad(self):
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'Tomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'Tomer')
        ItemsLogic.add_review_on_item('Tomer', 1, 'Good', 10)
        reviews = get_all_reviews_on_item(1)
        self.assertEqual(reviews, [])

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

    def test_bad_edit_shop_item(self):
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

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()