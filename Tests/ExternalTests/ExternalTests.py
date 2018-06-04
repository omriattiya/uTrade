import hashlib
import os
import unittest

from DomainLayer import UsersLogic, ShopLogic, ItemsLogic, UserShoppingCartLogic
from ExternalSystems import ExternalSystems,ProxyPaymentSystem,PaymentSystem,ProxySupplySystem,SupplySystem
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer.UsersLogic import register, edit_password, remove_user, login
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from SharedClasses.SystemManager import SystemManager


class ExternalTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')


    def test_payment_system(self):
        UsersLogic.register(RegisteredUser('ShaharBenS', "SsS0897SsS"))
        UsersLogic.update_details('ShaharBenS', 'AFG', 20, 'Male')

        UsersLogic.register(RegisteredUser('ShaharBenS2', "SsS0897SsS"))
        ShopLogic.create_shop(Shop('eBay', "Active"), 'ShaharBenS2')
        ShopLogic.create_shop(Shop('Amazon', "Active"), 'ShaharBenS2')
        item1 = Item(1, 'eBay', 'apple', 'vegas', 'good', 10, 500, 'regular', None, 0, 0, 0)
        item2 = Item(2, 'Amazon', 'apple', 'fruits', 'good', 10, 500, 'regular', None, 0, 0, 0)
        ItemsLogic.add_item_to_shop(item1, 'ShaharBenS2')
        ItemsLogic.add_item_to_shop(item2, 'ShaharBenS2')


        access_token = hashlib.md5('ShaharBenS'.encode()).hexdigest()
        Consumer.loggedInUsers[access_token] = 'ShaharBenS'
        Consumer.loggedInUsersShoppingCart[access_token] = []

        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ShaharBenS', 2, 3, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ShaharBenS', 1, 7, None))


        ExternalSystems.payment = ProxyPaymentSystem.ProxyPaymentSystem()
        status = UserShoppingCartLogic.pay_all(access_token)
        if isinstance(status,list) is not True:
            status = False
        self.assertFalse(status)

        ExternalSystems.payment = PaymentSystem.PaymentSystem()
        status = UserShoppingCartLogic.pay_all(access_token)
        if isinstance(status, list):
            status = True
        self.assertTrue(status)



    def test_supply_system(self):
        UsersLogic.register(RegisteredUser('ShaharBenS', "SsS0897SsS"))
        UsersLogic.update_details('ShaharBenS', 'AFG', 20, 'Male')

        UsersLogic.register(RegisteredUser('ShaharBenS2', "SsS0897SsS"))
        ShopLogic.create_shop(Shop('eBay', "Active"), 'ShaharBenS2')
        ShopLogic.create_shop(Shop('Amazon', "Active"), 'ShaharBenS2')
        item1 = Item(1, 'eBay', 'apple', 'vegas', 'good', 10, 500, 'regular', None, 0, 0, 0)
        item2 = Item(2, 'Amazon', 'apple', 'fruits', 'good', 10, 500, 'regular', None, 0, 0, 0)
        ItemsLogic.add_item_to_shop(item1, 'ShaharBenS2')
        ItemsLogic.add_item_to_shop(item2, 'ShaharBenS2')

        access_token = hashlib.md5('ShaharBenS'.encode()).hexdigest()
        Consumer.loggedInUsers[access_token] = 'ShaharBenS'
        Consumer.loggedInUsersShoppingCart[access_token] = []

        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ShaharBenS', 2, 3, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ShaharBenS', 1, 7, None))

        ExternalSystems.supply = ProxySupplySystem.ProxySupplySystem()
        status = UserShoppingCartLogic.pay_all(access_token)
        if isinstance(status, list) is not True:
            status = False
        self.assertFalse(status)

        ExternalSystems.supply = SupplySystem.SupplySystem()
        status = UserShoppingCartLogic.pay_all(access_token)
        if isinstance(status, list):
            status = True
        self.assertTrue(status)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
