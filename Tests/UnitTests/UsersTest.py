import unittest, os
from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.SystemManagers import add_system_manager
from DomainLayer.UsersLogic import register, edit_profile, remove_user, login
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.SystemManager import SystemManager


class UsersTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_login_good(self):
        register(RegisteredUser('ShaharShahar', '12341256'))
        status = login(RegisteredUser('ShaharShahar', '12341256'))
        self.assertTrue(status)

    def test_login_bad(self):
        register(RegisteredUser('Tomer123', '12345ABCDE'))
        status = login(RegisteredUser('Tomer123', '12345ABCDE1'))
        self.assertFalse(status)
        register(RegisteredUser('KingT678', '123456ABCabc'))
        status = login(RegisteredUser('KingT678', '123456ABCabcd'))
        self.assertFalse(status)


    def test_add_user(self):
        register(RegisteredUser('ShaharShahar', '12341256'))
        user = get_user('ShaharShahar')
        self.assertEqual(user.username, 'ShaharShahar')

    def test_add_bad_user(self):
        status = register(RegisteredUser('ShaharShahar', '1212'))
        self.assertFalse(status)

        status = register(RegisteredUser('Tomer!', '12121212'))
        self.assertFalse(status)

        status = register(RegisteredUser('Tomer@%', '12121212'))
        self.assertFalse(status)

        status = register(RegisteredUser('sa', '12361123'))
        self.assertFalse(status)

        status = register(RegisteredUser('', 'asdsada'))
        self.assertFalse(status)

    def test_add_existing_user(self):
        register(RegisteredUser('ShaharShahar', '12345126'))
        status = register(RegisteredUser('ShaharShahar', '11241324'))
        self.assertFalse(status)

    def test_edit_profile(self):
        register(RegisteredUser('TomerTomerLev', 'TomerTomer6969'))
        old_user = get_user('TomerTomerLev')
        user = RegisteredUser(old_user.username, 'newpass1234')
        status = edit_profile(user)
        self.assertTrue(status)
        new_user = get_user('TomerTomerLev')
        self.assertEqual(new_user.username, 'TomerTomerLev')

        status = edit_profile(RegisteredUser('ShaharShahar', '12345678'))
        self.assertFalse(status)

    def test_remove_user(self):
        register(RegisteredUser('YoniYoni', '12121122'))
        user = get_user('YoniYoni')
        self.assertEqual(user.username, 'YoniYoni')
        add_system_manager(SystemManager('YoniYonion', '123123123'))
        status = remove_user('YoniYonion', user.username)
        self.assertTrue(status)

    def test_bad_remove_user(self):
        register(RegisteredUser('YoniYoni', '12112212'))
        user = get_user('YoniYoni')
        self.assertEqual(user.username, 'YoniYoni')
        register(RegisteredUser('YoniYonion', '123123123'))
        remover = get_user('YoniYonion')
        status = remove_user(remover.username, user.username)
        self.assertFalse(status)

    def test_not_exist_remove_user(self):
        register(RegisteredUser('YoniYonion', '123123123'))
        remover = get_user('YoniYonion')
        add_system_manager(SystemManager('asdx123', '21431d1wd'))
        status = remove_user('asdx123', remover)
        self.assertFalse(status)

    def test_get_purchased_history(self):
        register(RegisteredUser('TomerTomer', '12121212'))
        user = get_user('TomerTomer')
        # add an item to Shopping cart
        # purchase
        # get purchased history
        # assertEqual(ans, [banana item])
        self.assertEqual(user, user)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
