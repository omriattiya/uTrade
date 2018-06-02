import hashlib
import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic, UserShoppingCartLogic
from DomainLayer.UsersLogic import register
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DomainLayer.ShoppingLogic import add_item_shopping_cart, remove_item_shopping_cart
from DomainLayer.UserShoppingCartLogic import pay_all
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from SharedClasses.StoreManager import StoreManager


class ShoppingTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100, 'regular',
                     "https://cdn3.iconfinder.com/data/icons/user-interface-icons-bundle-18/32/910-512.png", 0, 0, 0)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100, 'regular',
                     "https://cdn3.iconfinder.com/data/icons/user-interface-icons-bundle-18/32/910-512.png", 0, 0, 0)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        register(RegisteredUser('ToniToni', '1234567878'))
        username = 'ToniToni'
        access_token = hashlib.md5(username.encode()).hexdigest()
        Consumer.loggedInUsers[access_token] = username
        Consumer.loggedInUsersShoppingCart[access_token] = []
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem(username, item1.id, 3, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem(username, item2.id, 2, None))

    def test_pay_all(self):
        username = 'ToniToni'
        access_token = hashlib.md5(username.encode()).hexdigest()
        self.assertTrue(isinstance(pay_all(access_token), list))
        item1 = ItemsLogic.Items.search_item_in_shop('My Shop', 'milk')
        item2 = ItemsLogic.Items.search_item_in_shop('My Shop', 'steak')
        self.assertTrue(item1.quantity == 97)
        self.assertTrue(item2.quantity == 98)

    def test_pay_all_different_shops(self):
        register(RegisteredUser('YoniYoni1', '1234567878'))
        register(RegisteredUser('StoreManager11', '1234567878'))
        shop = Shop('My Shop1', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni1')
        UsersLogic.add_manager('YoniYoni1', StoreManager('StoreManager11', 'My Shop1', 1, 1, 1, 1, 1, 1, 1))
        item1 = Item(1, 'My Shop1', 'milk', 'diary', 'good', 12, 100, 'regular',
                     "https://cdn3.iconfinder.com/data/icons/user-interface-icons-bundle-18/32/910-512.png", 0, 0, 0)
        item2 = Item(2, 'My Shop1', 'steak', 'meat', 'bad', 12, 100, 'regular',
                     "https://cdn3.iconfinder.com/data/icons/user-interface-icons-bundle-18/32/910-512.png", 0, 0, 0)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager11')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager11')
        username = 'ToniToni'
        access_token = hashlib.md5(username.encode()).hexdigest()
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem(username, item1.id, 3, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem(username, item2.id, 2, None))
        self.assertTrue(isinstance(pay_all(access_token), list))

    def test_bad_no_items_cart_pay_all(self):
        item1 = ItemsLogic.Items.search_item_in_shop('My Shop', 'milk')
        item2 = ItemsLogic.Items.search_item_in_shop('My Shop', 'steak')
        username = 'ToniToni'
        access_token = hashlib.md5(username.encode()).hexdigest()
        UserShoppingCartLogic.remove_item_shopping_cart(access_token, item1.id)
        UserShoppingCartLogic.remove_item_shopping_cart(access_token, item2.id)
        self.assertEqual(pay_all(access_token), "Shopping cart is empty")

    def test_bad_out_of_stock_cart_pay_all(self):
        item3 = Item(3, 'My Shop', 'asado', 'meat', 'bad', 12, 100, 'regular',
                     "https://cdn3.iconfinder.com/data/icons/user-interface-icons-bundle-18/32/910-512.png", 0, 0, 0)
        ItemsLogic.add_item_to_shop(item3, 'StoreManager1')
        register(RegisteredUser('ToniToni1', '1234567878'))
        username = 'ToniToni'
        access_token = hashlib.md5(username.encode()).hexdigest()
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ToniToni', item3.id, 100, None))
        username1 = 'ToniToni1'
        access_token1 = hashlib.md5(username1.encode()).hexdigest()
        Consumer.loggedInUsers[access_token1] = username1
        Consumer.loggedInUsersShoppingCart[access_token1] = []
        UserShoppingCartLogic.add_item_shopping_cart(access_token1, ShoppingCartItem('ToniToni1', item3.id, 100, None))
        self.assertTrue(isinstance(pay_all(access_token), list))
        # TODO fix this test.
        self.assertEqual(pay_all(access_token1), "Only 0 asado exist in the system")

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
