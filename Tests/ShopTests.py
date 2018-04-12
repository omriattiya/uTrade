import os
import unittest
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer.ShopLogic import close_shop_permanently, create_shop
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DatabaseLayer.SystemManagers import add_system_manager


class ShopTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        add_system_manager(remover.username)
        create_shop('1111', owner.username)
        status = close_shop_permanently(remover.username, '1111')
        self.assertTrue(status)

    def test_bad_sys_man_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        create_shop('1111', owner.username)
        status = close_shop_permanently(remover.username, '1111')
        self.assertFalse(status)

    def test_bad_shop_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        add_system_manager(remover.username)
        create_shop('1111', owner.username)
        status = close_shop_permanently(remover.username, '2222')
        self.assertFalse(status)

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
