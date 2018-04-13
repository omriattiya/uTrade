import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DomainLayer.ShoppingLogic import add_item_shopping_cart, remove_item_shopping_cart
from DomainLayer.ShoppingLogic import pay_all


class ShoppingTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('Yoni', '12345678'))
        register(RegisteredUser('StoreManager1', '12345678'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'Yoni')
        UsersLogic.add_manager('Yoni', 'My Shop', 'StoreManager1', {
            'addItemPermission': 1,
            'removeItemPermission': 1,
            'editItemPermission': 1,
            'replyMessagePermission': 1,
            'getAllMessagePermission': 1,
            'getPurchaseHistoryPermission': 1
        })
        item1 = Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100)
        item2 = Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100)
        ItemsLogic.add_item_to_shop(item1, 'StoreManager1')
        ItemsLogic.add_item_to_shop(item2, 'StoreManager1')
        register(RegisteredUser('Toni', '12345678'))
        add_item_shopping_cart('Toni', item1.id, 3)
        add_item_shopping_cart('Toni', item2.id, 2)

    def test_pay_all(self):
        self.assertTrue(pay_all('Toni'))

    def test_bad_pay_all(self):
        item1 = ItemsLogic.Items.search_item_in_shop('My Shop', 'milk')
        item2 = ItemsLogic.Items.search_item_in_shop('My Shop', 'steak')
        remove_item_shopping_cart('Toni', item1.id)
        remove_item_shopping_cart('Toni', item2.id)
        self.assertFalse(pay_all('Toni'))

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
