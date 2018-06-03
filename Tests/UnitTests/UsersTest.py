import os
import unittest

from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer.UsersLogic import register, edit_password, remove_user, login
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.SystemManager import SystemManager


def returnStringToBoolean(status):
    if isinstance(status,bool):
        return status

    if len(status) > 5:
        if status[0:7] == 'SUCCESS':
            return True
        if status[0:6] == 'FAILED':
            return False
    return False


class UsersTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_login_good(self):
        register(RegisteredUser('ShaharShahar', '12341256'))
        status = login(RegisteredUser('ShaharShahar', '12341256'))
        self.assertTrue(returnStringToBoolean(status))

    def test_login_bad(self):
        register(RegisteredUser('Tomer123', '12345ABCDE'))
        status = login(RegisteredUser('Tomer123', '12345ABCDE1'))
        self.assertFalse(returnStringToBoolean(status))
        register(RegisteredUser('KingT678', '12345678ABCabc'))
        status = login(RegisteredUser('KingT678', '12345678ABCabcd'))
        self.assertFalse(returnStringToBoolean(status))

    def test_add_user(self):
        register(RegisteredUser('ShaharShahar', '12341256'))
        user = get_user('ShaharShahar')
        self.assertEqual(user.username, 'ShaharShahar')

    def test_add_bad_user(self):
        status = register(RegisteredUser('ShaharShahar', '1212'))
        self.assertFalse(returnStringToBoolean(status))

        status = register(RegisteredUser('Tomer!', '12121212'))
        self.assertFalse(returnStringToBoolean(status))

        status = register(RegisteredUser('Tomer@%', '12121212'))
        self.assertFalse(returnStringToBoolean(status))

        status = register(RegisteredUser('sa', '12361123'))
        self.assertFalse(returnStringToBoolean(status))

        status = register(RegisteredUser('', 'asdsada'))
        self.assertFalse(returnStringToBoolean(status))

    def test_add_existing_user(self):
        register(RegisteredUser('ShaharShahar', '12345126'))
        status = register(RegisteredUser('ShaharShahar', '11241324'))
        self.assertFalse(returnStringToBoolean(status))

    def test_edit_profile(self):
        register(RegisteredUser('TomerTomerLev', 'TomerTomer6969'))
        old_user = get_user('TomerTomerLev')
        user = RegisteredUser(old_user.username, 'newpass1234')
        status = edit_password(user)
        self.assertTrue(returnStringToBoolean(status))
        new_user = get_user('TomerTomerLev')
        self.assertEqual(new_user.username, 'TomerTomerLev')

    def test_bad_edit_profile(self):
        register(RegisteredUser('TomerTomerLev', 'TomerTomer6969'))
        status = edit_password(RegisteredUser('ShaharShahar', '1234567878'))
        self.assertFalse(returnStringToBoolean(status))

    def test_remove_user(self):
        register(RegisteredUser('YoniYoni', '12121122'))
        user = get_user('YoniYoni')
        self.assertEqual(user.username, 'YoniYoni')
        add_system_manager(SystemManager('YoniYonion', '123123123'))
        status = remove_user('YoniYonion', user)
        self.assertTrue(returnStringToBoolean(status))

    def test_bad_remover_remove_user(self):
        register(RegisteredUser('YoniYoni', '12112212'))
        user = get_user('YoniYoni')
        self.assertEqual(user.username, 'YoniYoni')
        register(RegisteredUser('YoniYonion', '123123123'))
        remover = get_user('YoniYonion')
        status = remove_user(remover.username, user)
        self.assertFalse(returnStringToBoolean(status))

    def test_bad_user_remove_user(self):
        register(RegisteredUser('YoniYoni', '12112212'))
        user = get_user('YoniYoni')
        self.assertEqual(user.username, 'YoniYoni')
        add_system_manager(SystemManager('YoniYonion', '123123123'))
        status = remove_user('YoniYonion', None)
        self.assertFalse(returnStringToBoolean(status))

    def test_not_exist_remove_user(self):
        add_system_manager(SystemManager('YoniYonion', '123123123'))
        status = remove_user('YoniYonion', RegisteredUser('sadasdf11', '123123123'))
        self.assertFalse(returnStringToBoolean(status))

    def test_get_purchased_history(self):
        register(RegisteredUser('TomerTomer', '12121212'))
        user = get_user('TomerTomer')
        # add an item to Shopping cart
        # purchase
        # get purchased history
        # assertEqual(ans, [banana item])
        self.assertEqual(user, user)

    def test_bad_get_purchased_history(self):
        register(RegisteredUser('TomerTomer', '12121212'))
        user = get_user('TomerTomer')
        # do not purchase anything
        # get purchased history
        # assertEqual(ans, [])
        self.assertEqual(user, user)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
