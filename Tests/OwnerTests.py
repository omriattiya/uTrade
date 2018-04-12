import unittest, os

from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, UsersLogic
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from DatabaseLayer import Owners, StoreManagers
from SharedClasses import Shop


class OwnerTests(unittest.TestCase):

    def setUp(self):
        init_database('db.sqlite3')

        username = 'Omri'
        register(RegisteredUser(username, '123456'))  # register user
        # ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), username)  # add shop
        # ItemsLogic.add_item_to_shop(Item.Item(1, shop_name, 'milk', 'milk', 'keywords', 1, 12, 100),
        #                           shop_name, username)

    def test_add_owner(self):
        username = 'Omri'
        shop_name = 'My New Shop'
        ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), username)  # add shop
        owner = Owners.get_owner(username, shop_name)
        self.assertEqual(len(owner), 1)
        self.assertEqual(owner[0][0], username)
        self.assertEqual(owner[0][1], shop_name)

    def test_add_owner_bad_owner(self):
        username = 'this username doesnt exist'
        shop_name = 'My New Shop'
        ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), 'Omri')  # add shop
        is_owner = Owners.get_owner(username, shop_name)
        self.assertFalse(is_owner)

    def test_add_owner_bad_shop(self):
        username = 'Omri'
        shop_name = 'bad shop name'
        ShopLogic.create_shop(Shop.Shop('My New Shop', 'ACTIVE'), username)  # add shop
        is_owner = Owners.get_owner(username, shop_name)
        self.assertFalse(is_owner)

    def test_add_manager(self):
        shop_name = 'bad shop name'
        target_user_name = 'Naruto'
        register(RegisteredUser(target_user_name, '123456'))  # register user
        permissions = {'addItemPermission': True,
                       'removeItemPermission': True,
                       'editItemPermission': True,
                       'replyMessagePermission': True,
                       'getAllMessagePermission': True,
                       'getPurchaseHistoryPermission': True
                       }
        ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), 'Omri')  # add shop
        store_manager = UsersLogic.add_manager('Omri', shop_name, target_user_name, permissions)
        self.assertEqual(store_manager, True)

    def test_add_manager_bad_username(self):
        shop_name = 'bad shop name'
        target_user_name = 'Naruto'
        permissions = {'addItemPermission': True,
                       'removeItemPermission': True,
                       'editItemPermission': True,
                       'replyMessagePermission': True,
                       'getAllMessagePermission': True,
                       'getPurchaseHistoryPermission': True
                       }
        store_manager = UsersLogic.add_manager('Omri',shop_name, target_user_name, permissions)
        self.assertFalse(store_manager)

    def test_add_manager_bad_shop(self):
        shop_name = 'bad shop name'
        target_user_name = 'Naruto'
        register(RegisteredUser(target_user_name, '123456'))  # register user
        permissions = {'addItemPermission': True,
                       'removeItemPermission': True,
                       'editItemPermission': True,
                       'replyMessagePermission': True,
                       'getAllMessagePermission': True,
                       'getPurchaseHistoryPermission': True
                       }
        ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), 'Omri')  # add shop
        store_manager = UsersLogic.add_manager('Omri',shop_name + '1', target_user_name, permissions)
        self.assertEqual(False, store_manager)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
