import os
import unittest

from DatabaseLayer.Auctions import get_all_auctions, get_max_bid
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, UsersLogic
from DomainLayer.AuctionLogic import add_auction, bid_on_item
from DomainLayer.UsersLogic import register
from SharedClasses.AuctionBid import AuctionBid
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.StoreManager import StoreManager


class AuctionTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('YoniYoni', '1234567878'))
        register(RegisteredUser('StoreManager1', '1234567878'))
        shop = Shop('My Shop', 'Active')
        ShopLogic.create_shop(shop, 'YoniYoni')
        UsersLogic.add_manager('YoniYoni', StoreManager('StoreManager1', 'My Shop', 1, 1, 1, 1, 1, 1, 1, 1))

    def test_add_auction(self):
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 1, 500, 'auction', None, 0, 0, 0)
        ret = add_auction(item1, 'StoreManager1', '2018-12-26')
        lst = get_all_auctions()
        self.assertTrue(ret is not False)
        self.assertTrue(len(lst) == 1)

    def test_bid_auction(self):
        register(RegisteredUser('Tomer1234', '1234567878'))
        register(RegisteredUser('Yoni1234', '1234567878'))
        register(RegisteredUser('Shahar1234', '1234567878'))
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 1, 1, 'auction', None, 0, 0, 0)
        ret = add_auction(item1, 'YoniYoni', '2018-12-26')
        self.assertTrue(ret is not False)
        ret = bid_on_item(AuctionBid(item1.id, 'Yoni1234', 100))
        self.assertTrue(ret is not False)
        ret = bid_on_item(AuctionBid(item1.id, 'Tomer1234', 1000))
        self.assertTrue(ret is not False)
        self.assertTrue(get_max_bid(item1.id) == 1000)

    def test_bad_add_auction(self):
        item1 = Item(1, 'My Shop', 'banana', 'vegas', 'good', 1, 500, 'auction', None, 0, 0, 0)
        ret = add_auction(item1, 'YoniYoni', '2011-12-26')
        lst = get_all_auctions()
        self.assertFalse(ret is not False)
        self.assertFalse(len(lst) == 1)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()