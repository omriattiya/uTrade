import os
import unittest
import time

from DatabaseLayer.PurchasedItems import add_purchased_item
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ReviewsOnItems import get_all_reviews_on_item
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer import PurchasedItems
from DomainLayer import ShopLogic, ItemsLogic
from DomainLayer.ItemsLogic import get_all_purchased_items
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop


class ItemsTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_get_all_purchased_items(self):
        register(RegisteredUser('Yoni', '121212'))
        user = get_user('Yoni')
        add_system_manager(user.username, user.password)
        add_purchased_item( "banana", 'Yoni')
        lst = get_all_purchased_items('Yoni')
        self.assertTrue(len(lst) > 0)

    def test_review_on_item(self):
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', "Open")
        ShopLogic.create_shop(shop, 'Tomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'Tomer')
        PurchasedItems.add_purchased_item(1, time.time(), 5, 10, 'Tomer')
        ItemsLogic.add_review_on_item('Tomer', 1, 'Good', 10)
        reviews = get_all_reviews_on_item(1)
        self.assertEqual(len(reviews), 1)

    def test_review_on_item_bad(self):
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', "Open")
        ShopLogic.create_shop(shop, 'Tomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'Tomer')
        ItemsLogic.add_review_on_item('Tomer', 1, 'Good', 10)
        reviews = get_all_reviews_on_item(1)
        self.assertEqual(reviews, [])

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
