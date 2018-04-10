from django.test import TestCase
from DatabaseLayer.initializeDatabase import init_database


class SearchTest(TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def search_by_name(self):
        # add user
        self.assertEqual(True, True)
        pass
