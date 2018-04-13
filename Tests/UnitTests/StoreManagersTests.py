import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import MessagingLogic, ItemsLogic, UsersLogic, SearchLogic, ShopLogic, ShoppingLogic
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.Item import Item
from DatabaseLayer import Shops, StoreManagers, Items


class StoreManagersTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_store_manager(self):
        UsersLogic.register(RegisteredUser('Shahar', '123456'))
        UsersLogic.register(RegisteredUser('TomerLev', '654321'))
        shop = Shop('myShop', 'Active')
        ShopLogic.create_shop(shop, 'Shahar')
        UsersLogic.add_manager('Shahar', 'myShop', 'TomerLev', {
            'addItemPermission': 1,
            'removeItemPermission': 1,
            'editItemPermission': 1,
            'replyMessagePermission': 1,
            'getAllMessagePermission': 1,
            'getPurchaseHistoryPermission': 1
        })
        manager = StoreManagers.get_store_manager('TomerLev', 'myShop')
        self.assertTrue(manager.permission_add_item > 0)
        self.assertTrue(manager.permission_remove_item > 0)
        self.assertTrue(manager.permission_edit_item > 0)
        self.assertEqual(manager.store_name, 'myShop')
        self.assertEqual(manager.username, 'TomerLev')

    def test_permissions(self):
        UsersLogic.register(RegisteredUser('Shahar', '123456'))
        UsersLogic.register(RegisteredUser('TomerLev', '654321'))
        shop = Shop('myShop', 'Active')
        ShopLogic.create_shop(shop, 'Shahar')
        UsersLogic.add_manager('Shahar', 'myShop', 'TomerLev', {
            'addItemPermission': 1,
            'removeItemPermission': 1,
            'editItemPermission': 1,
            'replyMessagePermission': 1,
            'getAllMessagePermission': 1,
            'getPurchaseHistoryPermission': 1
        })
        ItemsLogic.add_item_to_shop(Item(None, 'myShop', 'doll',
                                         'toys', 'toys:kids', 20, 300), 'TomerLev')
        item = Items.get_item(1)
        self.assertEqual(item.shop_name, 'myShop')
        self.assertEqual(item.price, 20)
        self.assertEqual(item.quantity, 300)

        status = ItemsLogic.edit_shop_item('TomerLev', 1, 'price', 40)
        self.assertTrue(status)
        status = ItemsLogic.edit_shop_item('TomerLev', 1, 'name', 'doll_new')
        self.assertTrue(status)
        status = ItemsLogic.edit_shop_item('TomerLev', 1, 'quantity', 40)
        self.assertTrue(status)

        item = Items.get_item(1)
        self.assertEqual(item.name,'doll_new')
        self.assertEqual(item.quantity,40)
        self.assertEqual(item.keyWords,'toys:kids')

        status = ItemsLogic.remove_item_from_shop(1, 'TomerLev')
        self.assertTrue(status)

    def test_no_permission(self):
        UsersLogic.register(RegisteredUser('Shahar', '123456'))
        UsersLogic.register(RegisteredUser('TomerLev', '654321'))
        shop = Shop('myShop', 'Active')
        ShopLogic.create_shop(shop, 'Shahar')
        UsersLogic.add_manager('Shahar', 'myShop', 'TomerLev', {
            'addItemPermission': 0,
            'removeItemPermission': 0,
            'editItemPermission': 0,
            'replyMessagePermission': 0,
            'getAllMessagePermission': 0,
            'getPurchaseHistoryPermission': 0
        })
        status = ItemsLogic.add_item_to_shop(Item(None, 'myShop', 'doll',
                                  'toys', 'toys;kids', 20, 300), 'TomerLev')
        self.assertFalse(status)

        status = MessagingLogic.send_message_from_shop('TomerLev', 'Hi There', 'myShop', 'Shahar')
        self.assertFalse(status)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
