import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer import Shops, ReviewsOnShops, ReviewsOnItems, PurchasedItems
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.ReviewsOnShops import get_all_reviews_on_shop
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic, UsersLogic
from DomainLayer.ShopLogic import close_shop_permanently, create_shop
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.ItemReview import ItemReview
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DatabaseLayer.SystemManagers import add_system_manager
from SharedClasses.ShopReview import ShopReview


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


    def test_pay_all(self):
        # TODO crate customer, fill cart, buy.
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, owner.username)
        status = True
        self.assertTrue(status)

    def test_bad_pay_all(self):
        # TODO crate customer, empty cart, buy.
        status = False
        self.assertFalse(status)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
