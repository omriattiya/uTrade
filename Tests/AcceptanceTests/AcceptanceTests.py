import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from Tests.AcceptanceTests import Bridge


class CusTomerTomer(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_register(self):  # 1.2
        is_added = Bridge.register_user('SHALOMSHALOM', '12345678')
        self.assertTrue(is_added)
        is_added = Bridge.register_user('SHALOMSHALOM', '12345678')
        self.assertFalse(is_added)

    def test_login(self):  # 1.8
        Bridge.register_user('SHALOMSHALOM', '12345678')
        is_logged = Bridge.login('SHALOMSHALOM', '12345678')
        self.assertTrue(is_logged)

    def test_open_shop(self):  # 1.9
        # register user
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        is_opened = Bridge.open_shop('username', 'shop_name')
        self.assertTrue(is_opened)
        # check if became owner
        is_owner = Bridge.is_owner('username', 'shop_name')
        self.assertTrue(is_owner)

    def test_cart_items(self):  # 1.5
        # open shop
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        Bridge.open_shop('username', 'shop_name')
        # item is = 1
        Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name1',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=100, username='username')
        # item is = 2
        Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name2',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=100, username='username')
        # item is = 3
        Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name3',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=100, username='username')

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=1, quantity=10)
        self.assertTrue(Bridge.is_item_bought(username='username', item_id=1))

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=2, quantity=10)
        self.assertTrue(Bridge.is_item_bought(username='username', item_id=2))

        Bridge.buy_item(username='username', shop_name='shop_name', item_id=3, quantity=10)
        self.assertTrue(Bridge.is_item_bought(username='username', item_id=3))

        is_bought = Bridge.buy_item(username='username', shop_name='shop_name', item_id=4, quantity=10)
        self.assertFalse(is_bought)

        is_bought = Bridge.buy_item(username='username', shop_name='shop_name', item_id=3, quantity=150)
        self.assertFalse(is_bought)

        # remove item from cart
        is_removed = Bridge.remove_item_from_cart(username='username', item_id=1)
        self.assertTrue(is_removed)

    def test_add_owner(self):  # 3.3
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        Bridge.open_shop('username', 'shop_name')
        Bridge.register_user('username1', 'password')
        Bridge.add_owner(owner='username', shop='shop_name', new_owner='username1')
        is_owner = Bridge.is_owner(username='username1', shop_name='shop_name')
        self.assertTrue(is_owner)

    def test_owner_add_items(self):  # 3.1
        # setup owner
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        Bridge.open_shop('username', 'shop_name')

        # owner add items
        # item is = 1
        is_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name1',
                                           item_category='item_category', keywords='keywords', price=10,
                                           quantity=100, username='username')
        self.assertTrue(is_added)
        # item is = 2
        is_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name2',
                                           item_category='item_category', keywords='keywords', price=10,
                                           quantity=100, username='username')
        self.assertTrue(is_added)
        # item is = 3
        is_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name3',
                                           item_category='item_category', keywords='keywords', price=10,
                                           quantity=100, username='username')
        self.assertTrue(is_added)

        is_edited = Bridge.edit_item_name(item_id=1, username='username', item_name='NEW NAME')
        self.assertTrue(is_edited)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
