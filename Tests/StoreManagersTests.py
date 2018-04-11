import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import MessagingLogic, ItemsLogic, UsersLogic, SearchLogic, ShopLogic, ShoppingLogic
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DatabaseLayer import Shops


class StoreManagersTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_store_manager(self):
        UsersLogic.register(RegisteredUser('Shahar', '123456'))
        UsersLogic.register(RegisteredUser('TomerLev', '654321'))
        shop = Shop('myShop', 0, 'Active')
        ShopLogic.create_shop(shop, 'Shahar')
        shop = Shops.get_shop('myShop')
        UsersLogic.add_manager('Shahar', shop, 'TomerLev', {
            'addItemPermission': 1,
            'removeItemPermission': 1,
            'editItemPermission': 1,
            'replyMessagePermission': 1,
            'getAllMessagePermission': 1,
            'getPurchaseHistoryPermission': 1
        })



    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
