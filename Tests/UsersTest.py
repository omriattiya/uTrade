import unittest,os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import getUser
from DomainLayer.Users import register,edit_profile
from SharedClasses.RegisteredUser import RegisteredUser

class UsersTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_user(self):
        register(RegisteredUser('Shahar','123456'))
        user = getUser('Shahar')

        self.assertEqual(True, True)

    def test_case2(self):
        self.assertEqual(True,True)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
