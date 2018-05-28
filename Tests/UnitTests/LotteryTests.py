import os
import unittest
from datetime import date


from DatabaseLayer.Lotteries import get_lotteries, get_lottery_customer
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ShoppingCartDB import add_item_shopping_cart
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, UsersLogic
from DomainLayer.LotteryLogic import add_lottery_and_items
from DomainLayer.ShoppingLogic import pay_all
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from SharedClasses.StoreManager import StoreManager
from SharedClasses.SystemManager import SystemManager


class LotteryTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))

    def test_add_lottery(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user = get_user('ToniToniToniToni')
        user1user1 = get_user('NoniNoni')
        add_system_manager(SystemManager(user.username, user.password))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'prize', None)
        item2 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'ticket', None)
        add_lottery_and_items(item1, item2, 500, date(2019, 12, 26), 'YoniYoni')
        lst = get_lotteries()
        self.assertTrue(len(lst) > 0)

    def test_add_lottery_customer(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user = get_user('ToniToniToniToni')
        user1user1 = get_user('NoniNoni')
        add_system_manager(SystemManager(user.username, user.password))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'prize', None)
        item2 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'ticket', None)
        add_lottery_and_items(item1, item2, 500, date(2019, 12, 26), 'YoniYoni')
        lst = get_lotteries()
        lottery = lst[0]
        add_item_shopping_cart(ShoppingCartItem('NoniNoni', lottery.lotto_id, 3, None))
        pay_all('NoniNoni')
        customer_lottery = get_lottery_customer(lottery.lotto_id, 'NoniNoni')
        self.assertTrue(customer_lottery is not False)

    def test_bad_date(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user = get_user('ToniToniToniToni')
        user1user1 = get_user('NoniNoni')
        add_system_manager(SystemManager(user.username, user.password))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'prize', None)
        item2 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'ticket', None)
        add_lottery_and_items(item1, item2, 500, date(2016, 12, 26), 'YoniYoni')
        lst = get_lotteries()
        lottery = lst[0]
        add_item_shopping_cart(ShoppingCartItem('NoniNoni', lottery.lotto_id, 3, None))
        pay_all('NoniNoni')
        customer_lottery = get_lottery_customer(lottery.lotto_id, 'NoniNoni')
        self.assertFalse(customer_lottery is not False)

    def test_bad_money(self):
        register(RegisteredUser('ToniToniToniToni', '12121212'))
        register(RegisteredUser('NoniNoni', '12121212'))
        user = get_user('ToniToniToniToni')
        user1user1 = get_user('NoniNoni')
        add_system_manager(SystemManager(user.username, user.password))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'prize', None)
        item2 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 10, 500, 'ticket', None)
        add_lottery_and_items(item1, item2, 1, date(2016, 12, 26), 'YoniYoni')
        lst = get_lotteries()
        lottery = lst[0]
        add_item_shopping_cart(ShoppingCartItem('NoniNoni', lottery.lotto_id, 3, None))
        pay_all('NoniNoni')
        customer_lottery = get_lottery_customer(lottery.lotto_id, 'NoniNoni')
        self.assertFalse(customer_lottery is not False)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
