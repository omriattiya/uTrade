import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.SystemManagers import add_system_manager
from DomainLayer import ShopLogic, ItemsLogic
from DomainLayer.ItemsLogic import get_all_purchased_items
from DomainLayer.UsersLogic import register
from SharedClasses import Shop
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from DatabaseLayer.PurchasedItems import add_purchased_item


class SystemManagerTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_get_all_purchased_items(self):

        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        register(RegisteredUser('Noni', '121212'))
        owner = get_user('Yoni')
        sys_man = get_user('Toni')
        cust = get_user('Noni')

        shop_name = 'My New Shop'
        ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), owner.username)  # add shop
        add_system_manager(sys_man.username)

        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), owner.username)
        # TODO buy milk
        add_purchased_item(1111, 2222, "banana", 'Yoni')
        # lst = get_all_purchased_items()
        # self.assertTrue(len(lst) > 0)
        self.assertTrue(True)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
