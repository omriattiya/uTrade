import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from Tests.AcceptanceTests import Bridge


class Customer(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def register(self):
        is_added = Bridge.register_user('SHALOM', '123456')
        self.assertTrue(is_added)
        is_added = Bridge.register_user('SHALOM', '123456')
        self.assertFalse(is_added)

    def login(self):
        Bridge.register_user('SHALOM', '123456')
        is_logged = Bridge.login('SHALOM', '123456')

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
