import unittest, os

from DatabaseLayer import ShoppingCart
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from DomainLayer import ShopLogic, ItemsLogic
from SharedClasses import Shop, Item


class ShoppingCartTests(unittest.TestCase):

    def setUp(self):
        init_database('db.sqlite3')

        username = 'Omri'
        shop_name = 'My New Shop'
        register(RegisteredUser(username, '123456'))  # register user
        ShopLogic.create_shop(Shop.Shop(shop_name, 1, 'ACTIVE'), username)  # add shop
        ItemsLogic.add_item_to_shop(Item.Item(1, shop_name, 'milk', 'milk', 'keywords', 1, 12, 100),
                                    shop_name, username)

    def test_add_item_to_cart(self):
        username = 'Omri'
        item_id = 1
        quantity = 20
        ShoppingCart.add_item_shopping_cart(username, item_id, quantity)
        cart_items = ShoppingCart.get_cart_items(username)  # [0] username [1] item_id [2] quantity
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0][0], username)
        self.assertEqual(cart_items[0][1], item_id)
        self.assertEqual(cart_items[0][2], quantity)

    def test_remove_item_from_cart(self):
        username = 'Omri'
        item_id = 1
        quantity = 20
        ShoppingCart.add_item_shopping_cart(username, item_id, quantity)
        ShoppingCart.remove_item_shopping_cart(username, item_id)
        cart_items = ShoppingCart.get_cart_items(username)  # [0] username [1] item_id [2] quantity
        self.assertEqual(len(cart_items), 0)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
