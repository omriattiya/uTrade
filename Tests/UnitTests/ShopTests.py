import os
import time
import unittest

from DatabaseLayer import Shops, ReviewsOnShops, ReviewsOnItems, PurchasedItems
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ReviewsOnShops import get_all_reviews_on_shop
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic
from DomainLayer.ShopLogic import close_shop_permanently, create_shop
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.ItemReview import ItemReview
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DatabaseLayer.SystemManagers import add_system_manager
from SharedClasses.ShopReview import ShopReview
from SharedClasses.SystemManager import SystemManager


class ShopTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_close_shop_permanently(self):
        register(RegisteredUser('YoniYoni', '12121212'))
        register(RegisteredUser('ToniToniToniToni', '12112212'))
        remover = get_user('YoniYoni')
        owner = get_user('ToniToniToniToni')
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, owner.username)
        add_system_manager(SystemManager(remover.username, remover.password))
        status = close_shop_permanently(remover.username, shop.name)
        self.assertTrue(status)

    def test_bad_sys_man_close_shop_permanently(self):
        register(RegisteredUser('YoniYoni', '12121122'))
        register(RegisteredUser('ToniToni', '12121122'))
        remover = get_user('YoniYoni')
        owner = get_user('ToniToni')
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, owner.username)
        status = close_shop_permanently(remover.username, 'My Shop')
        self.assertFalse(status)

    def test_bad_shop_close_shop_permanently(self):
        register(RegisteredUser('YoniYoni', '12121212'))
        register(RegisteredUser('ToniToni', '12121212'))
        remover = get_user('YoniYoni')
        owner = get_user('ToniToni')
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, owner.username)
        add_system_manager(SystemManager(remover.username, remover.password))
        status = close_shop_permanently(remover.username, 'My Shopi')
        self.assertFalse(status)

    def test_create_shop(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'TomerTomer')
        shop_founded = Shops.search_shop('My Shop')
        self.assertTrue(shop_founded.name == 'My Shop')

    def test_review_on_shop(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        user = get_user('TomerTomer')
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'TomerTomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'TomerTomer')
        PurchasedItems.add_purchased_item(1, time.time(), 5, 10, 'TomerTomer')
        shop_review = ShopReview('TomerTomer', 'Best', 10, 'My Shop')
        ShopLogic.add_review_on_shop(shop_review)
        reviews = get_all_reviews_on_shop('My Shop')
        self.assertEqual(len(reviews),1)

    def test_review_on_shop_bad(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        user = get_user('TomerTomer')
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, user)
        shop_review = ShopReview('TomerTomer', 'Best', 10, 'My Shop')
        ShopLogic.add_review_on_shop(shop_review)
        reviews = get_all_reviews_on_shop('My Shop')
        self.assertTrue(len(reviews) == 0)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()