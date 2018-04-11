import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import get_user
from DomainLayer.UsersLogic import register, edit_profile, remove_user, login
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

    def test_add_existing_user(self):
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

    def test_remove_user(self):
        register(RegisteredUser('Yoni', '121212'))
        user = get_user('Yoni')
        self.assertEqual(user.username, 'Yoni')
        register(RegisteredUser('Yonion', '123123123'))
        remover = get_user('Yoni')
        logged = login(remover)
        status = False
        if logged is True:
            status = remove_user(remover.username, user.username)
        self.assertTrue(status)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
