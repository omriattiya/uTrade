import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from Tests.AcceptanceTests import Bridge


class Customer(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def register(self):
        is_added = Bridge.register_user('SHALOM', '123456')
        self.assertTrue(is_added)
        is_added = Bridge.register_user('SHALOM', '123456')
        self.assertFalse(is_added)

    def login(self):
        Bridge.register_user('SHALOM', '123456')
        is_logged = Bridge.login('SHALOM', '123456')
        self.assertTrue(is_logged)

    def open_shop(self):
        # unregistered user
        is_opened = Bridge.open_shop('username', 'shop_name')
        self.assertFalse(is_opened)
        is_owner = Bridge.is_owner('username', 'shop_name')
        self.assertFalse(is_owner)
        # registered user
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        is_opened = Bridge.open_shop('username', 'shop_name')
        self.assertTrue(is_opened)
        # check if became owner
        is_owner = Bridge.is_owner('username', 'shop_name')
        self.assertTrue(is_owner)

    def buy_items(self):
        # open shop
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        Bridge.open_shop('username', 'shop_name')
        # item is = 1
        item_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name1',
                                             item_category='item_category', keywords='keywords', price=10,
                                             quantity=100, username='username')
        self.assertTrue(item_added)
        # item is = 2
        item_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name2',
                                             item_category='item_category', keywords='keywords', price=10,
                                             quantity=100, username='username')
        self.assertTrue(item_added)
        # item is = 3
        item_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name3',
                                             item_category='item_category', keywords='keywords', price=10,
                                             quantity=100, username='username')
        self.assertTrue(item_added)

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=1, quantity=10)
        self.assertTrue(Bridge.is_item_bought(username='username', item_id=1))

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=2, quantity=10)
        self.assertTrue(Bridge.is_item_bought(username='username', item_id=2))

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=3, quantity=10)
        self.assertTrue(Bridge.is_item_bought(username='username', item_id=3))

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=4, quantity=10)
        self.assertFalse(Bridge.is_item_bought(username='username', item_id=4))

        is_bought = Bridge.buy_item(username='username', shop_name='shop_name', item_id=3, quantity=150)
        self.assertFalse(is_bought)

    def

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
