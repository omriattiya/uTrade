import os
import unittest

from DatabaseLayer import Owners
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, UsersLogic
from SharedClasses import Shop
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.StoreManager import StoreManager


class OwnerTests(unittest.TestCase):

    def setUp(self):
        init_database(DB_NAME)
        UsersLogic.register(USER)

    def test_add_owner(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        owner = Owners.get_owner(USERNAME, SHOP.name)
        self.assertEqual(USERNAME, owner.username)
        self.assertEqual(SHOP.name, owner.shop_name)

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
        manager = StoreManager(OTHER_USERNAME, SHOP_NAME, PERMISSIONS[0], PERMISSIONS[1],
                               PERMISSIONS[2], PERMISSIONS[3], PERMISSIONS[4], PERMISSIONS[5], PERMISSIONS[6], )
        is_added = UsersLogic.add_manager(USERNAME, manager)
        self.assertTrue(is_added)

    def test_add_manager_bad_username(self):
        manager = StoreManager(OTHER_USERNAME, SHOP_NAME, PERMISSIONS[0], PERMISSIONS[1],
                               PERMISSIONS[2], PERMISSIONS[3], PERMISSIONS[4], PERMISSIONS[5], PERMISSIONS[6], )
        manager = StoreManager(OTHER_USERNAME, SHOP_NAME, PERMISSIONS[0], PERMISSIONS[1],
                               PERMISSIONS[2], PERMISSIONS[3], PERMISSIONS[4], PERMISSIONS[5], PERMISSIONS[6], )
        is_added = UsersLogic.add_manager(USERNAME, manager)
        self.assertFalse(is_added)

    def test_add_manager_bad_shop(self):
        ShopLogic.create_shop(SHOP, USERNAME)
        manager = StoreManager(OTHER_USERNAME, OTHER_SHOP_NAME, PERMISSIONS[0], PERMISSIONS[1], PERMISSIONS[2],
                               PERMISSIONS[3], PERMISSIONS[4], PERMISSIONS[5], PERMISSIONS[6], )
        is_added = UsersLogic.add_manager(USERNAME, manager)
        self.assertFalse(is_added)

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
        UsersLogic.modify_notifications(USERNAME, 0)
        owner = Owners.get_owner(USERNAME, SHOP_NAME)
        self.assertEqual(0, owner.should_notify)

        UsersLogic.modify_notifications(USERNAME, 1)
        owner = Owners.get_owner(USERNAME, SHOP_NAME)
        self.assertEqual(1, owner.should_notify)

    def tearDown(self):
        os.remove(DB_NAME)


if __name__ == '__main__':
    unittest.main()

DB_NAME = 'db.sqlite3'
PASSWORD = '12345126'
USERNAME = 'OmriOmri'
OTHER_USERNAME = 'NarutoNaruto'
SHOP_NAME = 'My New Shop'
OTHER_SHOP_NAME = 'Other Shop'
SHOP_STATUS = 'ACTIVE'
PERMISSIONS = [1, 1, 1, 1, 1, 1, 1]

SHOP = Shop.Shop(SHOP_NAME, SHOP_STATUS)
OTHER_SHOP = Shop.Shop(OTHER_SHOP_NAME, SHOP_STATUS)
USER = RegisteredUser(USERNAME, PASSWORD)
OTHER_USER = RegisteredUser(OTHER_USERNAME, PASSWORD)
