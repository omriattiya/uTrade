import os
import unittest
from datetime import datetime

from DatabaseLayer import Shops, PurchasedItems
from DatabaseLayer.Purchases import add_purchase_and_return_id
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ReviewsOnShops import get_all_reviews_on_shop
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic
from DomainLayer.ShopLogic import close_shop_permanently
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
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
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, owner.username)
        add_system_manager(SystemManager(remover.username, remover.password))
        status = close_shop_permanently(remover.username, shop.name)
        self.assertTrue(status)

    def test_bad_sys_man_close_shop_permanently(self):
        register(RegisteredUser('YoniYoni', '12121122'))
        register(RegisteredUser('ToniToni', '12121122'))
        remover = get_user('YoniYoni')
        owner = get_user('ToniToni')
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, owner.username)
        status = close_shop_permanently(remover.username, 'My Shop')
        self.assertFalse(status)

    def test_bad_shop_close_shop_permanently(self):
        register(RegisteredUser('YoniYoni', '12121212'))
        register(RegisteredUser('ToniToni', '12121212'))
        remover = get_user('YoniYoni')
        owner = get_user('ToniToni')
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, owner.username)
        add_system_manager(SystemManager(remover.username, remover.password))
        status = close_shop_permanently(remover.username, 'My Shopi')
        self.assertFalse(status)

    def test_create_shop(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'TomerTomer')
        shop_founded = Shops.search_shop('My Shop')
        self.assertTrue(shop_founded.name == 'My Shop')

    def test_bad_create_shop(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'TomerTomer')
        shop_founded = Shops.search_shop('My Shop')
        self.assertTrue(shop_founded.name == 'My Shop')
        status = ShopLogic.create_shop(shop, 'TomerTomer')
        self.assertEqual(status, 'FAILED: Shop name is taken')

    def test_review_on_shop(self):
        register(RegisteredUser('TomerTomer', '1234567878'))
        user = get_user('TomerTomer')
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'TomerTomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100, 'regular', None, 0, 0, 0),
                                    'TomerTomer')
        purchase_id = add_purchase_and_return_id(datetime.now(), 'TomerTomer', 0)
        status = PurchasedItems.add_purchased_item(purchase_id, 1, 10, 10)
        shop_review = ShopReview('TomerTomer', 'Best', 10, 'My Shop')
        status = ShopLogic.add_review_on_shop(shop_review)
        reviews = get_all_reviews_on_shop('My Shop')
        answer = len(reviews) == 1
        self.assertTrue(answer)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
