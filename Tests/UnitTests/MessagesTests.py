import os
import unittest

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
        UsersLogic.register(RegisteredUser('TomerTomer', '1234567878'))
        UsersLogic.register(RegisteredUser('ShaharShahar', '1234567878'))
        MessagingLogic.send_message(Message(1, 'TomerTomer', 'ShaharShahar', 'Hello 1'))
        MessagingLogic.send_message(Message(2, 'ShaharShahar', 'TomerTomer', 'Hello 2'))
        messages1 = MessagingLogic.get_all_messages('TomerTomer')
        messages2 = MessagingLogic.get_all_messages('ShaharShahar')
        self.assertTrue(messages1[0].content == 'Hello 2')
        self.assertTrue(messages2[0].content == 'Hello 1')

    def test_send_message_and_get_messages_of_shops(self):
        register(RegisteredUser('TomerTomer1', '1234567878'))
        shop1 = Shop('My Shop1', 'Active')
        ShopLogic.create_shop(shop1, 'TomerTomer1')
        register(RegisteredUser('TomerTomer2', '1234567878'))
        shop2 = Shop('My Shop2', 'Active')
        ShopLogic.create_shop(shop2, 'TomerTomer2')
        UsersLogic.add_manager('TomerTomer1', StoreManager('TomerTomer2', 'My Shop1', 1, 1, 1, 1, 1, 1, 1))
        UsersLogic.add_manager('TomerTomer2', StoreManager('TomerTomer1', 'My Shop2', 1, 1, 1, 1, 1, 1, 1))
        MessagingLogic.send_message_from_shop('TomerTomer2', Message(1, 'My Shop1', 'My Shop2', 'Hello 1'))
        MessagingLogic.send_message_from_shop('TomerTomer1', Message(2, 'My Shop2', 'My Shop1', 'Hello 2'))
        messages1 = MessagingLogic.get_all_shop_messages('TomerTomer2', 'My Shop1')
        messages2 = MessagingLogic.get_all_shop_messages('TomerTomer1', 'My Shop2')
        self.assertTrue(messages1[0].content == 'Hello 2')
        self.assertTrue(messages2[0].content == 'Hello 1')

    def test_bad_no_permssion_send_message_and_get_messages_of_shops(self):
        register(RegisteredUser('TomerTomer1', '1234567878'))
        shop1 = Shop('My Shop1', 'Active')
        ShopLogic.create_shop(shop1, 'TomerTomer1')
        register(RegisteredUser('TomerTomer2', '1234567878'))
        shop2 = Shop('My Shop2', 'Active')
        ShopLogic.create_shop(shop2, 'TomerTomer2')
        UsersLogic.add_manager('TomerTomer1', StoreManager('TomerTomer2', 'My Shop1', 1, 1, 1, 0, 1, 1, 1))
        UsersLogic.add_manager('TomerTomer2', StoreManager('TomerTomer1', 'My Shop2', 1, 1, 1, 0, 1, 1, 1))
        self.assertEqual(MessagingLogic.send_message_from_shop('TomerTomer2',
                                                               Message(1, 'My Shop1', 'My Shop2', 'Hello 1'))
                         , "FAILED: You don't have the permissions")
        self.assertEqual(MessagingLogic.send_message_from_shop('TomerTomer1',
                                                               Message(2, 'My Shop2', 'My Shop1', 'Hello 2'))
                         , "FAILED: You don't have the permissions")

    def test_bad_no_get_all_premss_send_message_and_get_messages_of_shops(self):
        register(RegisteredUser('TomerTomer1', '1234567878'))
        shop1 = Shop('My Shop1', 'Active')
        ShopLogic.create_shop(shop1, 'TomerTomer1')
        register(RegisteredUser('TomerTomer2', '1234567878'))
        shop2 = Shop('My Shop2', 'Active')
        ShopLogic.create_shop(shop2, 'TomerTomer2')
        UsersLogic.add_manager('TomerTomer1', StoreManager('TomerTomer2', 'My Shop1', 1, 1, 1, 1, 0, 1, 1))
        UsersLogic.add_manager('TomerTomer2', StoreManager('TomerTomer1', 'My Shop2', 1, 1, 1, 1, 0, 1, 1))
        MessagingLogic.send_message_from_shop('TomerTomer2', Message(1, 'My Shop1', 'My Shop2', 'Hello 1'))
        MessagingLogic.send_message_from_shop('TomerTomer1', Message(2, 'My Shop2', 'My Shop1', 'Hello 2'))
        messages1 = MessagingLogic.get_all_shop_messages('TomerTomer2', 'My Shop1')
        messages2 = MessagingLogic.get_all_shop_messages('TomerTomer1', 'My Shop2')
        self.assertFalse(messages1)
        self.assertFalse(messages2)

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
