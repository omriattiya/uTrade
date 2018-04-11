import unittest, os
from DatabaseLayer.initializeDatabase import init_database


class ShoppingTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_pay_all(self):
        # TODO crate customer, fill cart, buy.
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
