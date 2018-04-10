import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import getUser
from DomainLayer.Users import register, edit_profile
from SharedClasses.RegisteredUser import RegisteredUser


class UsersTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_add_user(self):
        register(RegisteredUser('Shahar', '123456',None))
        user = getUser('Shahar')
        self.assertEqual(user.username,'Shahar')
        self.assertEqual(user.password,'123456')
        self.assertEqual(user.role,'Customer')

    def test_add_bad_user(self):
        status = register(RegisteredUser('Shahar', '1236', None))
        self.assertFalse(status)

        status = register(RegisteredUser('12ahar', '1236123', None))
        self.assertFalse(status)

        status = register(RegisteredUser('', 'asdsada', None))
        self.assertFalse(status)

    def test_add_exisiting_user(self):
        register(RegisteredUser('Shahar', '123456',None))
        status = register(RegisteredUser('Shahar', '11241324',None))
        self.assertFalse(status)

    def test_edit_profile(self):
        register(RegisteredUser('TomerLev', 'tomer6969', None))
        old_user = getUser('TomerLev')
        user = RegisteredUser(old_user.username,'new_pass1234',None)
        status = edit_profile(user)
        self.assertTrue(status)
        new_user = getUser('TomerLev')
        self.assertEqual(new_user.username, 'TomerLev')
        self.assertEqual(new_user.password, 'new_pass1234')
        self.assertEqual(new_user.role, 'Customer')

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
