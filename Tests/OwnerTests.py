import unittest, os

from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, UsersLogic
from SharedClasses.RegisteredUser import RegisteredUser
from DatabaseLayer import Owners, StoreManagers
from SharedClasses import Shop


class OwnerTests(unittest.TestCase):

    def setUp(self):
        init_database(DB_NAME)
        UsersLogic.register(USER)

    def test_add_owner(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        owner = Owners.get_owner(USERNAME, SHOP.name)
        self.assertEqual(len(owner), 1)
        self.assertEqual(USERNAME, owner[0][0])
        self.assertEqual(SHOP.name, owner[0][1])

    def test_add_owner_bad_owner(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        is_owner = Owners.get_owner(OTHER_USERNAME, SHOP.name)
        self.assertFalse(is_owner)

    def test_add_owner_bad_shop(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        is_owner = Owners.get_owner(USERNAME, OTHER_SHOP_NAME)
        self.assertFalse(is_owner)

    def test_add_manager(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        UsersLogic.register(OTHER_USER)
        store_manager = UsersLogic.add_manager(USERNAME, SHOP_NAME, OTHER_USERNAME, PERMISSIONS)
        self.assertTrue(store_manager)

    def test_add_manager_bad_username(self):
        store_manager = UsersLogic.add_manager(USERNAME, SHOP_NAME, OTHER_USERNAME, PERMISSIONS)
        self.assertFalse(store_manager)

    def test_add_manager_bad_shop(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        store_manager = UsersLogic.add_manager(USERNAME, OTHER_SHOP_NAME, OTHER_USERNAME, PERMISSIONS)
        self.assertFalse(store_manager)

    def test_close_shop(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        self.assertTrue(UsersLogic.close_shop(USERNAME, SHOP_NAME))

    def test_close_shop_bad_owner(self):
        UsersLogic.register(OTHER_USER)
        ShopLogic.create_shop(SHOP, USERNAME)
        self.assertFalse(UsersLogic.close_shop(OTHER_USERNAME, SHOP_NAME))

    def test_close_shop_bad_shop_name(self):
        UsersLogic.register(OTHER_USER)
        ShopLogic.create_shop(OTHER_SHOP, OTHER_USERNAME)
        self.assertFalse(UsersLogic.close_shop(USERNAME, OTHER_SHOP_NAME))

    def test_re_open_shop(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        self.assertTrue(UsersLogic.re_open_shop(USERNAME, SHOP_NAME))

    def test_re_open_shop_bad_owner(self):
        UsersLogic.register(OTHER_USER)
        ShopLogic.create_shop(SHOP, USERNAME)
        self.assertFalse(UsersLogic.re_open_shop(OTHER_USERNAME, SHOP_NAME))

    def test_re_open_shop_bad_shop_name(self):
        UsersLogic.register(OTHER_USER)
        ShopLogic.create_shop(OTHER_SHOP, OTHER_USERNAME)
        self.assertFalse(UsersLogic.re_open_shop(USERNAME, OTHER_SHOP_NAME))

    def test_modify_notifications(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        UsersLogic.modify_notifications(USERNAME, 1)
        owner = Owners.get_owner(USERNAME, SHOP_NAME)
        self.assertEqual(1, owner[0][2])

        UsersLogic.modify_notifications(USERNAME, 0)
        owner = Owners.get_owner(USERNAME, SHOP_NAME)
        self.assertEqual(0, owner[0][2])

    def tearDown(self):
        os.remove(DB_NAME)


if __name__ == '__main__':
    unittest.main()

DB_NAME = 'db.sqlite3'
PASSWORD = '123456'
USERNAME = 'Omri'
OTHER_USERNAME = 'Naruto'
SHOP_NAME = 'My New Shop'
OTHER_SHOP_NAME = 'Other Shop'
SHOP_STATUS = 'ACTIVE'
PERMISSIONS = {'addItemPermission': True,
               'removeItemPermission': True,
               'editItemPermission': True,
               'replyMessagePermission': True,
               'getAllMessagePermission': True,
               'getPurchaseHistoryPermission': True
               }

SHOP = Shop.Shop(SHOP_NAME, SHOP_STATUS)
OTHER_SHOP = Shop.Shop(OTHER_SHOP_NAME, SHOP_STATUS)
USER = RegisteredUser(USERNAME, PASSWORD)
OTHER_USER = RegisteredUser(OTHER_USERNAME, PASSWORD)
