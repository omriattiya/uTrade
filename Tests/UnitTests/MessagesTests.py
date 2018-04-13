import os
import unittest

from DatabaseLayer import Messages
from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import MessagingLogic, ShopLogic, UsersLogic
from DomainLayer.UsersLogic import register
from SharedClasses.Message import Message
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.StoreManager import StoreManager


class MessageTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_send_message_and_get_messages_of_users(self):
        UsersLogic.register(RegisteredUser('Tomer', '12345678'))
        UsersLogic.register(RegisteredUser('Shahar', '12345678'))
        MessagingLogic.send_message(Message(1,'Tomer', 'Shahar', 'Hello 1'))
        MessagingLogic.send_message(Message(2,'Shahar', 'Tomer', 'Hello 2'))
        messages1 = MessagingLogic.get_all_messages('Tomer')
        messages2 = MessagingLogic.get_all_messages('Shahar')
        self.assertTrue(messages1[0].content == 'Hello 2')
        self.assertTrue(messages2[0].content == 'Hello 1')

    def test_send_message_and_get_messages_of_shops(self):
        register(RegisteredUser('Tomer1', '12345678'))
        shop1 = Shop('My Shop1', 'ACTIVE')
        ShopLogic.create_shop(shop1, 'Tomer1')
        register(RegisteredUser('Tomer2', '12345678'))
        shop2 = Shop('My Shop2', 'ACTIVE')
        ShopLogic.create_shop(shop2, 'Tomer2')
        UsersLogic.add_manager('Tomer1', StoreManager('Tomer2', 'My Shop1', 1, 1, 1, 1, 1, 1))
        UsersLogic.add_manager('Tomer2', StoreManager('Tomer1', 'My Shop2', 1, 1, 1, 1, 1, 1))
        MessagingLogic.send_message_from_shop('Tomer2',Message(1,'My Shop1','My Shop2','Hello 1'))
        MessagingLogic.send_message_from_shop('Tomer1',Message(2,'My Shop2','My Shop1','Hello 2'))
        messages1 = MessagingLogic.get_all_shop_messages('Tomer2','My Shop1')
        messages2 = MessagingLogic.get_all_shop_messages('Tomer1','My Shop2')
        self.assertTrue(messages1[0].content == 'Hello 2')
        self.assertTrue(messages2[0].content == 'Hello 1')

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
