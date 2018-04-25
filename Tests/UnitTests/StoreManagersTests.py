import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import MessagingLogic, ItemsLogic, UsersLogic, SearchLogic, ShopLogic, ShoppingLogic
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.Item import Item
from SharedClasses.StoreManager import StoreManager
from SharedClasses.Message import Message
from DatabaseLayer import Shops, StoreManagers, Items


class StoreManagersTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_store_manager(self):
        UsersLogic.register(RegisteredUser('ShaharShahar', '12345126'))
        UsersLogic.register(RegisteredUser('TomerTomerLev', '65412321'))
        shop = Shop('myShop', 'Active')
        ShopLogic.create_shop(shop, 'ShaharShahar')
        UsersLogic.add_manager('ShaharShahar', StoreManager('TomerTomerLev', 'myShop', 1, 1, 1, 1, 1, 1, 1))
        manager = StoreManagers.get_store_manager('TomerTomerLev', 'myShop')
        self.assertTrue(manager.permission_add_item > 0)
        self.assertTrue(manager.permission_remove_item > 0)
        self.assertTrue(manager.permission_edit_item > 0)
        self.assertEqual(manager.store_name, 'myShop')
        self.assertEqual(manager.username, 'TomerTomerLev')

    def test_permissions(self):
        UsersLogic.register(RegisteredUser('ShaharShahar', '1212345678'))
        UsersLogic.register(RegisteredUser('TomerTomerLev', '65412321'))
        shop = Shop('myShop', 'Active')
        ShopLogic.create_shop(shop, 'ShaharShahar')
        UsersLogic.add_manager('ShaharShahar', StoreManager('TomerTomerLev', 'myShop', 1, 1, 1, 1, 1, 1, 1))
        ItemsLogic.add_item_to_shop(Item(None, 'myShop', 'doll',
                                         'toys', 'toys:kids', 20, 300, 'regular'), 'TomerTomerLev')
        item = Items.get_item(1)
        self.assertEqual(item.shop_name, 'myShop')
        self.assertEqual(item.price, 20)
        self.assertEqual(item.quantity, 300)

        status = ItemsLogic.edit_shop_item('TomerTomerLev', 1, 'price', 40)
        self.assertTrue(status)
        status = ItemsLogic.edit_shop_item('TomerTomerLev', 1, 'name', 'doll_new')
        self.assertTrue(status)
        status = ItemsLogic.edit_shop_item('TomerTomerLev', 1, 'quantity', 40)
        self.assertTrue(status)

        item = Items.get_item(1)
        self.assertEqual(item.name, 'doll_new')
        self.assertEqual(item.quantity, 40)
        self.assertEqual(item.keyWords, 'toys:kids')

        status = ItemsLogic.remove_item_from_shop(1, 'TomerTomerLev')
        self.assertTrue(status)

    def test_no_permission(self):
        UsersLogic.register(RegisteredUser('ShaharShahar', '12312456'))
        UsersLogic.register(RegisteredUser('TomerTomerLev', '65431221'))
        shop = Shop('myShop', 'Active')
        ShopLogic.create_shop(shop, 'ShaharShahar')
        UsersLogic.add_manager('ShaharShahar', StoreManager('TomerTomerLev', 'myShop', 0, 0, 0, 0, 0, 0, 0))
        status = ItemsLogic.add_item_to_shop(Item(None, 'myShop', 'doll',
                                                  'toys', 'toys;kids', 20, 300, 'regular'), 'TomerTomerLev')
        self.assertFalse(status)

        message = Message(None, 'myShop', 'ShaharShahar', 'Hi There')
        status = MessagingLogic.send_message_from_shop('TomerTomerLev', message)
        self.assertFalse(status)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()