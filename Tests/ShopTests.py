import os
import unittest
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer.ShopLogic import close_shop_permanently, create_shop
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop


class ShopTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        # TODO set Yoni as Sys_Manager then try to close shop
        user = get_user('Yoni')
        create_shop('1111', user.username)
        status = close_shop_permanently(user.username, '1111')
        self.assertTrue(status)

    def test_create_shop(self):
        register(RegisteredUser('Tomer', '12345678'))
        user = get_user('Tomer')
        shop = Shop(123, 'My Shop', 20, "Open")
        create_shop(shop, user)
        self.assertTrue(True)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
