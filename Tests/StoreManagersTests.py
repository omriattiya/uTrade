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
        username = 'Shahar'
        UsersLogic.register(RegisteredUser(username, '123456'))
        shop = Shop('myShop', 0, 'Active')
        ShopLogic.create_shop(shop,username)
        shop = Shops.get_shop(1)
        UsersLogic.add_manager(username,)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
