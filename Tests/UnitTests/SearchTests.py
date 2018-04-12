import os
import unittest
from DatabaseLayer import Shops
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import ShopLogic, ItemsLogic, SearchLogic
from DomainLayer.UsersLogic import register
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop


class SearchTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        register(RegisteredUser('Tomer', '12345678'))
        shop = Shop('My Shop', 'ACTIVE')
        ShopLogic.create_shop(shop, 'Tomer')
        ItemsLogic.add_item_to_shop(Item(1, 'My Shop', 'milk', 'diary', 'good', 12, 100), 'Tomer')
        ItemsLogic.add_item_to_shop(Item(2, 'My Shop', 'steak', 'meat', 'bad', 12, 100), 'Tomer')
        ItemsLogic.add_item_to_shop(Item(3, 'My Shop', 'banana', 'fruit', 'best', 12, 100), 'Tomer')
        ItemsLogic.add_item_to_shop(Item(3, 'My Shop', 'water', 'drinks', 'one two', 12, 100), 'Tomer')

    def test_search_shop(self):
        shop_founded = Shops.search_shop('My Shop')
        self.assertTrue(shop_founded.name == 'My Shop')

    def test_search_item_in_shop(self):
        items_founded = SearchLogic.search_item_in_shop('My Shop', 'banana')
        self.assertTrue(items_founded[0][2] == 'banana')

    def test_search_item_by_name(self):
        items_founded = SearchLogic.search_by_name('banana')
        self.assertTrue(items_founded[0][2] == 'banana')
        items_founded = SearchLogic.search_by_name('milk')
        self.assertTrue(items_founded[0][2] == 'milk')
        items_founded = SearchLogic.search_by_name('steak')
        self.assertTrue(items_founded[0][2] == 'steak')

    def test_search_item_by_category(self):
        items_founded = SearchLogic.search_by_category('diary')
        self.assertTrue(items_founded[0][2] == 'milk')
        self.assertTrue(items_founded[0][3] == 'diary')
        items_founded = SearchLogic.search_by_category('meat')
        self.assertTrue(items_founded[0][2] == 'steak')
        self.assertTrue(items_founded[0][3] == 'meat')
        items_founded = SearchLogic.search_by_category('fruit')
        self.assertTrue(items_founded[0][2] == 'banana')
        self.assertTrue(items_founded[0][3] == 'fruit')

    def test_search_item_by_keywords(self):
        items_founded = SearchLogic.search_by_keywords('good')
        self.assertTrue(items_founded[0][2] == 'milk')
        self.assertTrue(items_founded[0][3] == 'diary')
        items_founded = SearchLogic.search_by_keywords('bad')
        self.assertTrue(items_founded[0][2] == 'steak')
        self.assertTrue(items_founded[0][3] == 'meat')
        items_founded = SearchLogic.search_by_keywords('best')
        self.assertTrue(items_founded[0][2] == 'banana')
        self.assertTrue(items_founded[0][3] == 'fruit')
        items_founded = SearchLogic.search_by_keywords('one;two')
        self.assertTrue(items_founded[0][2] == 'water')
        self.assertTrue(items_founded[0][3] == 'drinks')


    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
