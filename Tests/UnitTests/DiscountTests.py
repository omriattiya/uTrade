import unittest, os

from datetime import date
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.Discount import add_visible_discount
from DatabaseLayer.Discount import add_invisible_discount
from DatabaseLayer.Discount import get_visible_discount
from DatabaseLayer.Discount import get_invisible_discount
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.StoreManager import StoreManager
from SharedClasses.VisibleDiscount import VisibleDiscount
from SharedClasses.InvisibleDiscount import InvisibleDiscount


class ShoppingTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_visible_discount(self):
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100, 'regular')
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        disc = VisibleDiscount(item1.id, shop.name, 0.5, date(2018, 12, 26), date(2019, 12, 26))
        self.assertTrue(add_visible_discount(disc))

    def test_add_invisible_discount(self):
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100, 'regular')
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        invdisc = InvisibleDiscount('ABCDEFGHIJKLMNO',item1.id, shop.name, 0.5, date(2018, 12, 26), date(2019, 12, 26))
        self.assertTrue(add_invisible_discount(invdisc))

    def test_get_visible_discount(self):
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100, 'regular')
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        disc = VisibleDiscount(item1.id, shop.name, 0.5, date(2017, 12, 26), date(2019, 12, 26))
        self.assertTrue(add_visible_discount(disc))
        getted = get_visible_discount(item1.id, shop.name)
        self.assertEqual(getted.item_id, disc.item_id)
        self.assertEqual(getted.shop_name, disc.shop_name)
        self.assertEqual(getted.percentage, disc.percentage)

    def test_get_invisible_discount(self):
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100, 'regular')
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        invdisc = InvisibleDiscount('ABCDEFGHIJKLMNO', item1.id, shop.name, 0.5, date(2017, 12, 26), date(2019, 12, 26))
        self.assertTrue(add_invisible_discount(invdisc))
        getted = get_invisible_discount(item1.id, shop.name, 'ABCDEFGHIJKLMNO')
        self.assertEqual(getted.item_id, invdisc.item_id)
        self.assertEqual(getted.shop_name, invdisc.shop_name)
        self.assertEqual(getted.percentage, invdisc.percentage)
        self.assertEqual(getted.code, invdisc.code)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
