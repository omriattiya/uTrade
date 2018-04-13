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
        ShopLogic.create_shop(Shop.Shop(shop_name, 'ACTIVE'), username)  # add shop
        ItemsLogic.add_item_to_shop(Item.Item(1, shop_name, 'milk', 'milk', 'keywords', 12, 100), username)
        ItemsLogic.add_item_to_shop(Item.Item(2, shop_name, 'glue', 'glue', 'keywords', 12, 100), username)

    def test_add_item_to_cart(self):
        username = 'Omri'
        item_id = 1
        quantity = 20
        ShoppingCart.add_item_shopping_cart(ShoppingCart.ShoppingCart(username, item_id, quantity, ""))
        cart_items = ShoppingCart.get_cart_items(username)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0].username, username)
        self.assertEqual(cart_items[0].item_id, item_id)
        self.assertEqual(cart_items[0].item_quantity, quantity)

    def test_remove_item_from_cart(self):
        username = 'Omri'
        item_id = 1
        quantity = 20
        ShoppingCart.add_item_shopping_cart(ShoppingCart.ShoppingCart(username, item_id, quantity, ""))
        ShoppingCart.remove_item_shopping_cart(username, item_id)
        cart_items = ShoppingCart.get_cart_items(username)
        self.assertEqual(len(cart_items), 0)

    def test_get_cart_items(self):
        username = 'Omri'
        item_id1 = 1
        quantity1 = 20
        item_id2 = 2
        quantity2 = 2
        ShoppingCart.add_item_shopping_cart(ShoppingCart.ShoppingCart(username, item_id1, quantity1, ""))
        ShoppingCart.add_item_shopping_cart(ShoppingCart.ShoppingCart(username, item_id2, quantity2, ""))
        cart_items = ShoppingCart.get_cart_items(username)
        self.assertEqual(len(cart_items), 2)
        self.assertEqual(username, cart_items[0].username)
        self.assertEqual(item_id1, cart_items[0].item_id)
        self.assertEqual(quantity1, cart_items[0].item_quantity)
        self.assertEqual(username, cart_items[1].username)
        self.assertEqual(item_id2, cart_items[1].item_id)
        self.assertEqual(quantity2, cart_items[1].item_quantity)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
