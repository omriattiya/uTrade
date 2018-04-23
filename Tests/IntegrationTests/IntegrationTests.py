import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer import RegisteredUsers, Owners, StoreManagers
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.SystemManager import SystemManager
from SharedClasses.Shop import Shop
from SharedClasses.Owner import Owner
from SharedClasses.StoreManager import StoreManager
from SharedClasses.Item import Item
from SharedClasses.Message import Message
from SharedClasses.ShoppingCart import ShoppingCart
from SharedClasses.ItemReview import ItemReview
from DomainLayer import UsersLogic, ShopLogic, ShoppingLogic, ItemsLogic, SearchLogic, MessagingLogic


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_torture1(self):
        # Adding Users
        status = UsersLogic.register(RegisteredUser('user1user1', 'asdas12da'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('user2user2', 'cse12fdsf'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('user3user3', '12312124'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('user4user4', '1344321324'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('user5user5', '1c24c143c1'))
        self.assertTrue(status)

        # Adding System Managers
        status = UsersLogic.add_system_manager(SystemManager('sys1sys1', 'POWER123'))
        self.assertTrue(status)

        status = UsersLogic.edit_profile(RegisteredUser('user5user5', '12312456'))
        self.assertTrue(status)

        user = RegisteredUsers.get_user('user5user5')

        UsersLogic.remove_user('sys1sys1', user.username)
        status = RegisteredUsers.get_user('user5user5')
        self.assertFalse(status)

    def test_torture2(self):
        # Adding Users
        status = UsersLogic.register(RegisteredUser('u1ser1u1ser1', 'wxde12exd12'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u2ser2u2ser2', '34c124c1'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u3ser3u3ser3', '1c241c24c1'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u4ser4u4ser4', '3214v132v4132'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u5seru5ser', '12121212'))
        self.assertTrue(status)

        # Adding System Managers
        status = UsersLogic.add_system_manager(SystemManager('sys1sys1', 'POWER123'))
        self.assertTrue(status)

        # Creating Shops
        status = ShopLogic.create_shop(Shop('myShop1', 'ACTIVE'), 'u1ser1u1ser1')
        self.assertTrue(status)

        status = ShopLogic.create_shop(Shop('myShop2', 'ACTIVE'), 'u2ser2u2ser2')
        self.assertTrue(status)

        status = UsersLogic.add_owner('u1ser1u1ser1', Owner('u3ser3u3ser3', 'myShop1', 0))
        self.assertTrue(status)

        owner = Owners.get_owner('u1ser1u1ser1', 'myShop1')
        status = UsersLogic.add_manager(
            owner.username, StoreManager('u4ser4u4ser4', 'myShop1', 1, 1, 1, 1, 1, 1))
        status = UsersLogic.add_manager(
            'u2ser2u2ser2', StoreManager('u4ser4u4ser4', 'myShop2', 1, 1, 1, 1, 1, 1)
        )

        manager = StoreManagers.get_store_manager('u4ser4u4ser4', 'myShop1')

        self.assertEqual(manager.permission_reply_messages, 1)

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'banana', 'fruits', 'fruit;healthy;yellow', 4.90, 300), 'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'doll', 'toys', 'fun', 30, 10), 'u2ser2u2ser2')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'soda', 'drinks', 'good', 4.90, 20), 'u1ser1u1ser1')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'cucumber', 'vegetables', 'fun', 4.90, 300), 'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'vodka', 'drinks', 'bad;for;your;health', 70, 2), 'u3ser3u3ser3')

        items = SearchLogic.search_by_name('banana')
        self.assertEqual(items[0].quantity, 300)
        self.assertEqual(items[0].price, 4.90)
        self.assertEqual(len(items), 1)

        items = SearchLogic.search_by_category('drinks')
        self.assertEqual(items[0].quantity, 20)
        self.assertEqual(items[1].price, 70)
        self.assertEqual(len(items), 2)

        items = SearchLogic.search_by_keywords('fun')
        self.assertEqual(items[0].quantity, 10)
        self.assertEqual(items[1].price, 4.90)
        self.assertEqual(len(items), 2)

        items = SearchLogic.search_items_in_shop('myShop2')
        self.assertEqual(items[0].name, 'doll')
        self.assertEqual(items[1].name, 'cucumber')
        self.assertEqual(len(items), 2)

        MessagingLogic.send_message_from_shop('u4ser4u4ser4',
                                              Message(None, 'myShop1', 'u5seru5ser', 'Nadav is our lord and savior'))
        messages = MessagingLogic.get_all_messages('u5seru5ser')
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, 'Nadav is our lord and savior')

        MessagingLogic.send_message(Message(None, 'u5seru5ser', 'myShop1', 'Hello Shop'))
        messages = MessagingLogic.get_all_shop_messages('u4ser4u4ser4', 'myShop1')
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, 'Hello Shop')

        MessagingLogic.send_message_from_shop('u1ser1u1ser1', Message(None, 'myShop1', 'myShop2', 'Hello Shop2'))
        messages = MessagingLogic.get_all_shop_messages('u2ser2u2ser2', 'myShop2')
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, 'Hello Shop2')

        MessagingLogic.send_message(Message(None, 'u1ser1u1ser1', 'sys1sys1', 'Shop2 Sucks!'))
        messages = MessagingLogic.get_all_messages('sys1sys1')
        self.assertEqual(messages[0].content, 'Shop2 Sucks!')

        UsersLogic.close_shop('u1ser1u1ser1', 'myShop1')
        items = SearchLogic.search_by_name('banana')
        self.assertEqual(len(items), 0)

    def test_torture3(self):
        # Adding Users
        status = UsersLogic.register(RegisteredUser('u1ser1u1ser1', 'wxde12exd12'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u2ser2u2ser2', '34c124c1'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u3ser3u3ser3', '1c241c24c1'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u4ser4u4ser4', '3214v132v4132'))
        self.assertTrue(status)
        status = UsersLogic.register(RegisteredUser('u5seru5ser', '12121212'))
        self.assertTrue(status)

        # Adding System Managers
        status = UsersLogic.add_system_manager(SystemManager('sys1sys1', 'POWER123'))
        self.assertTrue(status)

        # Creating Shops
        status = ShopLogic.create_shop(Shop('myShop1', 'ACTIVE'), 'u1ser1u1ser1')
        self.assertTrue(status)

        status = ShopLogic.create_shop(Shop('myShop2', 'ACTIVE'), 'u2ser2u2ser2')
        self.assertTrue(status)

        status = UsersLogic.add_owner('u1ser1u1ser1', Owner('u3ser3u3ser3', 'myShop1', 0))
        self.assertTrue(status)

        owner = Owners.get_owner('u1ser1u1ser1', 'myShop1')
        status = UsersLogic.add_manager(
            owner.username, StoreManager('u4ser4u4ser4', 'myShop1', 1, 1, 1, 1, 1, 1))
        status = UsersLogic.add_manager(
            'u2ser2u2ser2', StoreManager('u4ser4u4ser4', 'myShop2', 1, 1, 1, 1, 1, 1)
        )

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'banana', 'fruits', 'fruit;healthy;yellow', 4.90, 300), 'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'doll', 'toys', 'fun', 30, 10), 'u2ser2u2ser2')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'soda', 'drinks', 'good', 4.90, 20), 'u1ser1u1ser1')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'cucumber', 'vegetables', 'fun', 4.90, 300), 'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'vodka', 'drinks', 'bad;for;your;health', 70, 2), 'u3ser3u3ser3')

        ShoppingLogic.add_item_shopping_cart(ShoppingCart('u5seru5ser', 1, 10, None))
        ShoppingLogic.add_item_shopping_cart(ShoppingCart('u5seru5ser', 2, 5, None))
        ShoppingLogic.add_item_shopping_cart(ShoppingCart('u5seru5ser', 3, 15, None))

        items = ShoppingLogic.get_cart_items('u5seru5ser')
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].code, None)

        ShoppingLogic.remove_item_shopping_cart('u5seru5ser', 1)
        items = ShoppingLogic.get_cart_items('u5seru5ser')
        self.assertEqual(len(items), 2)

        ShoppingLogic.remove_item_shopping_cart('u5seru5ser', 2)
        items = ShoppingLogic.get_cart_items('u5seru5ser')
        self.assertEqual(len(items), 1)

        # Only item id 3 left

        ShoppingLogic.pay_all('u5seru5ser')
        items1 = UsersLogic.get_purchase_history('u5seru5ser')
        items2 = ItemsLogic.get_all_purchased_items('sys1sys1')
        items3 = ShopLogic.get_shop_purchase_history('u4ser4u4ser4','myShop1')
        self.assertEqual(items1[0].item_id,items2[0].item_id)
        self.assertEqual(items2[0].quantity,items3[0].quantity)
        self.assertEqual(items1[0].price,items3[0].price)

        self.assertTrue('Nadav Ha Gever')

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
