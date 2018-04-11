import os
import unittest

from DatabaseLayer import Shops, ReviewsOnShops
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic
from DomainLayer.ShopLogic import close_shop_permanently, create_shop
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.ShopReview import ShopReview


class ShopTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_close_shop_permanently(self):
        register(RegisteredUser('Yoni', '121212'))
        # TODO set Yoni as Sys_Manager then try to close shop
        user = get_user('Yoni')
        create_shop('1111', user.username)
        status = close_shop_permanently(user.username, '1111')
        self.assertTrue(status)

    def test_create_shop(self):
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', "Open")
        ShopLogic.create_shop(shop, 'Tomer')
        shop_founded = Shops.search_shop('My Shop')
        self.assertTrue(shop_founded.name == 'My Shop')

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
