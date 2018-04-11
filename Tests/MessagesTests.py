import os
import unittest

from DatabaseLayer import Messages
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import MessagingLogic, ShopLogic
from DomainLayer.UsersLogic import register
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop


class MessageTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_send_message_and_get_messages_of_users(self):
        register(RegisteredUser('Tomer', '12345678'))
        register(RegisteredUser('Shahar', '12345678'))
        MessagingLogic.send_message('Tomer', 'Shahar', 'Hello 1')
        MessagingLogic.send_message('Shahar', 'Tomer', 'Hello 2')
        messages1 = MessagingLogic.get_all_messages('Tomer')
        messages2 = MessagingLogic.get_all_messages('Shahar')
        self.assertTrue(messages1[0][3] == 'Hello 2')
        self.assertTrue(messages2[0][3] == 'Hello 1')

    def test_send_message_and_get_messages_of_shops(self):
        register(RegisteredUser('Tomer', '12345678'))
        user1 = get_user('Tomer')
        shop1 = Shop('My Shop1', "Open")
        ShopLogic.create_shop(shop1, user1)
        register(RegisteredUser('Shahar', '12345678'))
        user2 = get_user('Shahar')
        shop2 = Shop('My Shop2', "Open")
        ShopLogic.create_shop(shop2, user2)
        MessagingLogic.send_message_from_shop('Tomer','Hello 1', 'My Shop1','My Shop2')
        MessagingLogic.send_message_from_shop('Shahar','Hello 2', 'My Shop2','My Shop1')
        messages1 = MessagingLogic.get_all_shop_messages('Tomer','My Shop1')
        messages2 = MessagingLogic.get_all_shop_messages('Shahar','My Shop2')
        self.assertTrue(messages1[0][3] == 'Hello 2')
        self.assertTrue(messages2[0][3] == 'Hello 1')

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
