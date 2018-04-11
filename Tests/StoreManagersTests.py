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
        self.assertTrue(manager[2] > 0)
        self.assertTrue(manager[3] > 0)
        self.assertTrue(manager[4] > 0)
        self.assertEqual(manager[1], 'myShop')
        self.assertEqual(manager[0], 'TomerLev')

    def test_add_item_permission(self):
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
                                         'toys', ['toys', 'kids'], 20, 300), 'TomerLev')
        item = Items.get_item(1)
        keywords = item.keyWords
        self.assertEqual(item.shop_name,'myShop')
        self.assertEqual(item.price,20)
        self.assertEqual(item.quantity,300)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
