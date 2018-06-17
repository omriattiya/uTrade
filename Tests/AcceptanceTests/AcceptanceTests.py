import hashlib
import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from ServiceLayer.services.LiveAlerts import Consumer
from Tests.AcceptanceTests import Bridge


class CusTomerTomer(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_register(self):  # 1.2
        # success scenario
        is_added = Bridge.register_user('SHALOMSHALOM', '12345678')
        self.assertTrue(is_added)
        # sad scenario
        is_added = Bridge.register_user('SHALOMSHALOM', '12345678')
        self.assertEqual(is_added, 'FAILED: Username is already taken')

    def test_login(self):  # 1.8
        Bridge.register_user('SHALOMSHALOM', '12345678')
        is_logged = Bridge.login('SHALOMSHALOM', '12345678')
        self.assertTrue(is_logged)

        # sad scenario
        is_logged = Bridge.login('SHALOMSHALOM', '123456789')
        self.assertEqual(is_logged, 'FAILED:Password in incorrect')

    def test_open_shop(self):  # 1.9
        # register user
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        is_opened = Bridge.open_shop('username', 'shop_name')
        self.assertTrue(is_opened)
        # check if became owner
        is_owner = Bridge.is_owner('username', 'shop_name')
        self.assertTrue(is_owner)

        # sad scenario - existing shop name
        is_opened = Bridge.open_shop('username', 'shop_name')
        self.assertEqual(is_opened, 'FAILED: Shop name is taken')

    def test_cart_items(self):  # 1.5
        # open shop
        Bridge.register_user('username', 'password')
        Bridge.login('username', 'password')
        Bridge.open_shop('username', 'shop_name')
        # item is = 1
        Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name1',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=100, username='username', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        # item is = 2
        Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name2',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=100, username='username', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        # item is = 3
        Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name3',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=100, username='username', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        username = 'username'
        access_token = hashlib.md5(username.encode()).hexdigest()
        Consumer.loggedInUsers[access_token] = username
        Consumer.loggedInUsersShoppingCart[access_token] = []
        Bridge.buy_item(login_token=access_token, username='username', shop_name='shop_name', item_id=1, quantity=10)
        self.assertTrue(Bridge.is_item_bought(login_token=access_token, item_id=1))

        Bridge.buy_item(login_token=access_token, username='username', shop_name='shop_name', item_id=2, quantity=10)
        self.assertTrue(Bridge.is_item_bought(login_token=access_token, item_id=2))

        Bridge.buy_item(login_token=access_token, username='username', shop_name='shop_name', item_id=3, quantity=10)
        self.assertTrue(Bridge.is_item_bought(login_token=access_token, item_id=3))

        is_bought = Bridge.buy_item(login_token=access_token, username='username', shop_name='shop_name', item_id=4,
                                    quantity=10)
        self.assertFalse(is_bought)

        is_bought = Bridge.buy_item(login_token=access_token, username='username', shop_name='shop_name', item_id=3,
                                    quantity=150)
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
                                           quantity=100, username='username', kind='regular', url=None,
                                           item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        self.assertTrue(is_added)
        # item is = 2
        is_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name2',
                                           item_category='item_category', keywords='keywords', price=10,
                                           quantity=100, username='username', kind='regular', url=None,
                                           item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        self.assertTrue(is_added)
        # item is = 3
        is_added = Bridge.add_item_to_shop(shop_name='shop_name', item_name='item_name3',
                                           item_category='item_category', keywords='keywords', price=10,
                                           quantity=100, username='username', kind='regular', url=None,
                                           item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        self.assertTrue(is_added)

        is_edited = Bridge.edit_item_name(item_id=1, username='username', item_name='NEW NAME')
        self.assertTrue(is_edited)

    def test_buy(self):  # 1.7
        # setup shop
        Bridge.register_user('ownerUser', 'password')
        Bridge.login('ownerUser', 'password')
        Bridge.open_shop('ownerUser', 'my_shop')
        Bridge.register_user('clientUser', 'password')
        Bridge.search_shop('my_shop')

        # add items to shop
        Bridge.add_item_to_shop(shop_name='my_shop', item_name='item_name1',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=10, username='ownerUser', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        Bridge.add_item_to_shop(shop_name='my_shop', item_name='item_name2',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=20, username='ownerUser', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        Bridge.add_item_to_shop(shop_name='my_shop', item_name='item_name3',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=30, username='ownerUser', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        Bridge.add_item_to_shop(shop_name='my_shop', item_name='item_name4',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=40, username='ownerUser', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)
        Bridge.add_item_to_shop(shop_name='my_shop', item_name='item_name5',
                                item_category='item_category', keywords='keywords', price=10,
                                quantity=50, username='ownerUser', kind='regular', url=None,
                                item_rating=0, sum_of_ranking=0, num_of_reviews=0)

        # add items to cart
        username = 'clientUser'
        access_token = hashlib.md5(username.encode()).hexdigest()
        Consumer.loggedInUsers[access_token] = username
        Consumer.loggedInUsersShoppingCart[access_token] = []
        Bridge.buy_item(access_token, 'clientUser', 'my_shop', 1, 10)
        Bridge.buy_item(access_token, 'clientUser', 'my_shop', 2, 10)
        Bridge.buy_item(access_token, 'clientUser', 'my_shop', 3, 10)
        Bridge.buy_item(access_token, 'clientUser', 'my_shop', 4, 10)
        Bridge.buy_item(access_token, 'clientUser', 'my_shop', 5, 10)

        # check total cost is calculated right
        self.assertEqual(Bridge.get_cart_cost(access_token), 500)

        # buy!
        self.assertTrue(Bridge.pay_cart(access_token))

        # check quantity in store changed
        self.assertEqual(Bridge.quantity_in_store(1), 0)
        self.assertEqual(Bridge.quantity_in_store(2), 10)
        self.assertEqual(Bridge.quantity_in_store(3), 20)
        self.assertEqual(Bridge.quantity_in_store(4), 30)
        self.assertEqual(Bridge.quantity_in_store(5), 40)
        # alternative scenario - item quantity is not enough
        self.assertFalse(Bridge.buy_item(access_token, 'clientUser', 'my_shop', 1, 10))

        # alternative scenario - added items, but another user already bought them
        username2 = 'clientUser2'
        access_token2 = hashlib.md5(username2.encode()).hexdigest()
        Consumer.loggedInUsers[access_token2] = username2
        Consumer.loggedInUsersShoppingCart[access_token2] = []
        Bridge.register_user('clientUser2', 'password')
        Bridge.buy_item(access_token, 'clientUser', 'my_shop', 2, 10)
        Bridge.buy_item(access_token2, 'clientUser2', 'my_shop', 2, 10)

        self.assertTrue(isinstance(Bridge.pay_cart(access_token2), list))
        self.assertTrue(isinstance(Bridge.pay_cart(access_token), str))

    def test_system_remove(self):  # 5.2
        # check sys manager really exist
        self.assertTrue(Bridge.is_system_manager('Ultimate_OmriOmri',
                                                 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f'))

        # add a normal user
        self.assertTrue(Bridge.register_user('normalUser', 'password'))

        # delete the normal user
        self.assertTrue(Bridge.delete_user(by='Ultimate_OmriOmri', who='normalUser'))
        self.assertEqual(Bridge.login('normalUser', 'password'), 'FAILED: Username is incorrect')

        # add owner of store
        Bridge.register_user('ownerUser', 'password')
        Bridge.open_shop('ownerUser', 'myShop')

        # delete owner and its shop
        self.assertTrue(Bridge.delete_user(by='Ultimate_OmriOmri', who='ownerUser'))
        self.assertEqual(Bridge.login('normalUser', 'password'), 'FAILED: Username is incorrect')

        shop = Bridge.search_shop('myShop')
        self.assertEqual(shop.status, "Permanently_closed")

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
