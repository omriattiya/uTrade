import hashlib
import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from DatabaseLayer import RegisteredUsers, Owners, StoreManagers
from ServiceLayer.services.LiveAlerts import Consumer
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.SystemManager import SystemManager
from SharedClasses.Shop import Shop
from SharedClasses.Owner import Owner
from SharedClasses.StoreManager import StoreManager
from SharedClasses.Item import Item
from SharedClasses.Message import Message
from SharedClasses.ShoppingCartItem import ShoppingCartItem
from SharedClasses.ItemReview import ItemReview
from DomainLayer import UsersLogic, ShopLogic, ShoppingLogic, ItemsLogic, SearchLogic, MessagingLogic, \
    UserShoppingCartLogic, ShoppingPolicyLogic


def StoB(status):
    if isinstance(status,bool):
        return status

    if len(status) > 5:
        if status[0:7] == 'SUCCESS':
            return True
        if status[0:6] == 'FAILED':
            return False
    elif len(status) == 2 and isinstance(status[0], int) and isinstance(status[1], float):
        return True
    return False


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

        status = UsersLogic.edit_password(RegisteredUser('user5user5', '12312456'))
        self.assertTrue(status)

        user = RegisteredUsers.get_user('user5user5')

        UsersLogic.remove_user('sys1sys1', user)
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
        status = ShopLogic.create_shop(Shop('myShop1', 'Active'), 'u1ser1u1ser1')
        self.assertTrue(status)

        status = ShopLogic.create_shop(Shop('myShop2', 'Active'), 'u2ser2u2ser2')
        self.assertTrue(status)

        status = UsersLogic.add_owner('u1ser1u1ser1', Owner('u3ser3u3ser3', 'myShop1', 0))
        self.assertTrue(status)

        owner = Owners.get_owner('u1ser1u1ser1', 'myShop1')
        status = UsersLogic.add_manager(
            owner.username, StoreManager('u4ser4u4ser4', 'myShop1', 1, 1, 1, 1, 1, 1, 1))
        status = UsersLogic.add_manager(
            'u2ser2u2ser2', StoreManager('u4ser4u4ser4', 'myShop2', 1, 1, 1, 1, 1, 1, 1)
        )

        manager = StoreManagers.get_store_manager('u4ser4u4ser4', 'myShop1')

        self.assertEqual(manager.permission_reply_messages, 1)

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'banana', 'fruits', 'fruit;healthy;yellow', 4.90, 300, 'regular', None, 0, 0, 0),
            'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'doll', 'toys', 'fun', 30, 10, 'regular', None, 0, 0, 0), 'u2ser2u2ser2')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'soda', 'drinks', 'good', 4.90, 20, 'regular', None, 0, 0, 0), 'u1ser1u1ser1')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'cucumber', 'vegetables', 'fun', 4.90, 300, 'regular', None, 0, 0, 0), 'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'vodka', 'drinks', 'bad;for;your;health', 70, 2, 'regular', None, 0, 0, 0),
            'u3ser3u3ser3')

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

        MessagingLogic.send_message(Message(None, 'u1ser1u1ser1', 'u3ser3u3ser3', 'Shop2 Sucks!'))
        messages = MessagingLogic.get_all_messages('u3ser3u3ser3')
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
        status = ShopLogic.create_shop(Shop('myShop1', 'Active'), 'u1ser1u1ser1')
        self.assertTrue(status)

        status = ShopLogic.create_shop(Shop('myShop2', 'Active'), 'u2ser2u2ser2')
        self.assertTrue(status)

        status = UsersLogic.add_owner('u1ser1u1ser1', Owner('u3ser3u3ser3', 'myShop1', 0))
        self.assertTrue(status)

        owner = Owners.get_owner('u1ser1u1ser1', 'myShop1')
        status = UsersLogic.add_manager(
            owner.username, StoreManager('u4ser4u4ser4', 'myShop1', 1, 1, 1, 1, 1, 1, 1))
        status = UsersLogic.add_manager(
            'u2ser2u2ser2', StoreManager('u4ser4u4ser4', 'myShop2', 1, 1, 1, 1, 1, 1, 1)
        )

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'banana', 'fruits', 'fruit;healthy;yellow', 4.90, 300, 'regular', None, 0, 0, 0),
            'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'doll', 'toys', 'fun', 30, 10, 'regular', None, 0, 0, 0), 'u2ser2u2ser2')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'soda', 'drinks', 'good', 4.90, 20, 'regular', None, 0, 0, 0), 'u1ser1u1ser1')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop2', 'cucumber', 'vegetables', 'fun', 4.90, 300, 'regular', None, 0, 0, 0), 'u4ser4u4ser4')

        ItemsLogic.add_item_to_shop(
            Item(None, 'myShop1', 'vodka', 'drinks', 'bad;for;your;health', 70, 2, 'regular', None, 0, 0, 0),
            'u3ser3u3ser3')
        username1 = 'u4ser4u4ser4'
        username2 = 'u2ser2u2ser2'
        username3 = 'u1ser1u1ser1'
        username4 = 'u3ser3u3ser3'
        username5 = 'u5seru5ser'

        access_token1 = hashlib.md5(username1.encode()).hexdigest()
        Consumer.loggedInUsers[access_token1] = username1
        Consumer.loggedInUsersShoppingCart[access_token1] = []

        access_token2 = hashlib.md5(username2.encode()).hexdigest()
        Consumer.loggedInUsers[access_token2] = username2
        Consumer.loggedInUsersShoppingCart[access_token2] = []

        access_token3 = hashlib.md5(username3.encode()).hexdigest()
        Consumer.loggedInUsers[access_token3] = username3
        Consumer.loggedInUsersShoppingCart[access_token3] = []

        access_token4 = hashlib.md5(username4.encode()).hexdigest()
        Consumer.loggedInUsers[access_token4] = username4
        Consumer.loggedInUsersShoppingCart[access_token4] = []

        access_token5 = hashlib.md5(username5.encode()).hexdigest()
        Consumer.loggedInUsers[access_token5] = username5
        Consumer.loggedInUsersShoppingCart[access_token5] = []

        UserShoppingCartLogic.add_item_shopping_cart(access_token5, ShoppingCartItem('u5seru5ser', 1, 10, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token5, ShoppingCartItem('u5seru5ser', 2, 5, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token5, ShoppingCartItem('u5seru5ser', 3, 15, None))

        items = UserShoppingCartLogic.get_cart_items(access_token5)
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].code, None)

        UserShoppingCartLogic.remove_item_shopping_cart(access_token5, 1)
        items = UserShoppingCartLogic.get_cart_items(access_token5)
        self.assertEqual(len(items), 2)

        UserShoppingCartLogic.remove_item_shopping_cart(access_token5, 2)
        items = UserShoppingCartLogic.get_cart_items(access_token5)
        self.assertEqual(len(items), 1)

        # Only item id 3 left

        UserShoppingCartLogic.pay_all(access_token5)
        items1 = UsersLogic.get_purchase_history('u5seru5ser')
        items2 = ItemsLogic.get_all_purchased_items('sys1sys1')
        items3 = ShopLogic.get_shop_purchase_history('u4ser4u4ser4', 'myShop1')
        self.assertEqual(items1[0].item_id, items2[0].item_id)
        self.assertEqual(items2[0].quantity, items3[0].quantity)
        self.assertEqual(items1[0].price, items3[0].price)

        self.assertTrue('Nadav Ha Gever')

    def test_policies(self):
        UsersLogic.register(RegisteredUser('ShaharBenS', "SsS0897SsS"))
        UsersLogic.update_details('ShaharBenS', 'AFG', 20, 'Male')

        UsersLogic.register(RegisteredUser('ShaharBenS2', "SsS0897SsS"))
        ShopLogic.create_shop(Shop('eBay', "Active"), 'ShaharBenS2')
        ShopLogic.create_shop(Shop('Amazon', "Active"), 'ShaharBenS2')
        item1 = Item(1, 'eBay', 'apple', 'vegas', 'good', 10, 500, 'regular', None, 0, 0, 0)
        item2 = Item(2, 'Amazon', 'apple', 'fruits', 'good', 10, 500, 'regular', None, 0, 0, 0)
        ItemsLogic.add_item_to_shop(item1, 'ShaharBenS2')
        ItemsLogic.add_item_to_shop(item2, 'ShaharBenS2')

        ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'eBay', "age = ''20''", "AL", 3)
        ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'Amazon', "age > ''15''", "UT", 5)
        ShoppingPolicyLogic.add_shopping_policy_on_identity('Ultimate_ShaharShahar', "sex = ''Male''", "AL", 9)
        ShoppingPolicyLogic.add_shopping_policy_on_category('Ultimate_ShaharShahar', "vegas", "state = ''AFG''", "UT", 5)
        ShoppingPolicyLogic.add_shopping_policy_on_items('Ultimate_ShaharShahar', "apple", "state != ''AFG''", "E", 2)

        access_token = hashlib.md5('ShaharBenS'.encode()).hexdigest()
        Consumer.loggedInUsers[access_token] = 'ShaharBenS'
        Consumer.loggedInUsersShoppingCart[access_token] = []

        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ShaharBenS', 2, 3, None))
        UserShoppingCartLogic.add_item_shopping_cart(access_token, ShoppingCartItem('ShaharBenS', 1, 7, None))
        status = UserShoppingCartLogic.pay_all(access_token)
        print(status)
        self.assertFalse(StoB(status))

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
