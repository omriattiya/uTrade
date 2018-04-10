import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import get_user
from DomainLayer.UsersLogic import register, edit_profile
from SharedClasses.RegisteredUser import RegisteredUser


class UsersTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_user(self):
        register(RegisteredUser('Shahar', '123456'))
        user = get_user('Shahar')
        self.assertEqual(user.username,'Shahar')
        self.assertEqual(user.password,'123456')

    def test_add_bad_user(self):
        status = register(RegisteredUser('Shahar', '1236'))
        self.assertFalse(status)

        status = register(RegisteredUser('12ahar', '1236123'))
        self.assertFalse(status)

        status = register(RegisteredUser('', 'asdsada'))
        self.assertFalse(status)

    def test_add_exisiting_user(self):
        register(RegisteredUser('Shahar', '123456'))
        status = register(RegisteredUser('Shahar', '11241324'))
        self.assertFalse(status)

    def test_edit_profile(self):
        register(RegisteredUser('TomerLev', 'tomer6969'))
        old_user = get_user('TomerLev')
        user = RegisteredUser(old_user.username,'new_pass1234')
        status = edit_profile(user)
        self.assertTrue(status)
        new_user = get_user('TomerLev')
        self.assertEqual(new_user.username, 'TomerLev')
        self.assertEqual(new_user.password, 'new_pass1234')

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
