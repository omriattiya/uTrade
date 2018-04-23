import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DomainLayer.ShoppingLogic import add_item_shopping_cart, remove_item_shopping_cart
from DomainLayer.ShoppingLogic import pay_all
from SharedClasses.ShoppingCart import ShoppingCart
from SharedClasses.StoreManager import StoreManager


class ShoppingTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        register(RegisteredUser('ToniToni', '1234567878'))
        add_item_shopping_cart(ShoppingCart('ToniToni', item1.id, 3, None))
        add_item_shopping_cart(ShoppingCart('ToniToni', item2.id, 2, None))

    def test_pay_all(self):
        self.assertTrue(pay_all('ToniToni'))

    def test_bad_pay_all(self):
        item1 = ItemsLogic.Items.search_item_in_shop('My Shop', 'milk')
        item2 = ItemsLogic.Items.search_item_in_shop('My Shop', 'steak')
        remove_item_shopping_cart('ToniToni', item1.id)
        remove_item_shopping_cart('ToniToni', item2.id)
        self.assertFalse(pay_all('ToniToni'))

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
