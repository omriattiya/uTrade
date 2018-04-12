import os
import unittest

from DatabaseLayer import Shops, ReviewsOnShops, ReviewsOnItems
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic
from DomainLayer.ShopLogic import close_shop_permanently, create_shop
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.ItemReview import ItemReview
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from DatabaseLayer.SystemManagers import add_system_manager
from SharedClasses.ShopReview import ShopReview


class ShopTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        add_system_manager(remover.username)
        create_shop('1111', owner.username)
        status = close_shop_permanently(remover.username, '1111')
        self.assertTrue(status)

    def test_bad_sys_man_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        create_shop('1111', owner.username)
        status = close_shop_permanently(remover.username, '1111')
        self.assertFalse(status)

    def test_bad_shop_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        register(RegisteredUser('Toni', '121212'))
        remover = get_user('Yoni')
        owner = get_user('Toni')
        add_system_manager(remover.username)
        create_shop('1111', owner.username)
        status = close_shop_permanently(remover.username, '2222')
        self.assertFalse(status)

    def test_create_shop(self):
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', "Open")
        ShopLogic.create_shop(shop, 'Tomer')
        shop_founded = Shops.search_shop('My Shop')
        self.assertTrue(shop_founded.name == 'My Shop')

    def test_review_on_item(self):
        register(RegisteredUser('Tomer', '12345678'))
        user = get_user('Tomer')
        item = Item('Tomer', 'My Shop', 'Banana', 'Fruit', 'Bad', 5, 5)
        item_review = ItemReview('Tomer', 'Good', 3, 1)
        ReviewsOnItems.add_review_on_item('Tomer', item.id, 'Best', 10)
        self.assertTrue(True)

    def test_review_on_shop(self):
        register(RegisteredUser('Tomer', '12345678'))
        user = get_user('Tomer')
        shop = Shop('My Shop', "Open")
        ShopLogic.create_shop(shop, user)
        shop_review = ShopReview('Tomer', 'Best', 10, 'My Shop')
        ReviewsOnShops.add_review_on_shop(shop_review.writerId, shop_review.shop_name, shop_review.description, shop_review.rank)
        self.assertTrue(True)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
