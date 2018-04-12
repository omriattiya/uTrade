import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.SystemManagers import add_system_manager
from DomainLayer.ItemsLogic import get_all_purchased_items
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from DatabaseLayer.PurchasedItems import add_purchased_item


class ItemsTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_get_all_purchased_items(self):
        register(RegisteredUser('Yoni', '121212'))
        user = get_user('Yoni')
        add_system_manager(user.username)
        add_purchased_item(1111, 2222, "banana", 'Yoni')
        lst = get_all_purchased_items()
        self.assertTrue(len(lst) > 0)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
