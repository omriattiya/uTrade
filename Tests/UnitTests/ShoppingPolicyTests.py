import os
import unittest

from DatabaseLayer.RegisteredUsers import get_user
from DatabaseLayer.SystemManagers import add_system_manager
from DatabaseLayer.initializeDatabase import init_database
from DomainLayer import UsersLogic, ShopLogic, ItemsLogic, ShoppingPolicyLogic
from SharedClasses.ShoppingPolicyOnShop import ShoppingPolicyOnShop
from SharedClasses.Item import Item
from SharedClasses.RegisteredUser import RegisteredUser
from SharedClasses.Shop import Shop
from SharedClasses.SystemManager import SystemManager


def StoB(status):
    if isinstance(status, bool):
        return status

    if len(status) > 5:
        if status[0:7] is 'SUCCESS':
            return True
        if status[0:6] is 'FAILED':
            return True
    return False


# Ultimate_ShaharShahar, ADMINISTRATOR

class UsersTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')
        UsersLogic.register(RegisteredUser('ShaharBenS', "SsS0897SsS"))
        UsersLogic.update_details('ShaharBenS', 'AFG', 20, 'Male')

        UsersLogic.register(RegisteredUser('ShaharBenS2', "SsS0897SsS"))
        ShopLogic.create_shop(Shop('eBay', "Active"), 'ShaharBenS2')
        item1 = Item(1, 'eBay', 'banana', 'vegas', 'good', 10, 500, 'regular', None, 0, 0, 0)
        ItemsLogic.add_item_to_shop(item1, 'ShaharBenS2')

    def test_add_get_policy(self):
        status = ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'eBay', "", "N", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'eBay', "", "UT", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_identity('Ultimate_ShaharShahar', "", "N", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_identity('Ultimate_ShaharShahar', "", "N", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_category('Ultimate_ShaharShahar', "", "", "N", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_category('Ultimate_ShaharShahar', "", "", "N", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_items('Ultimate_ShaharShahar', "", "", "N", 0)
        self.assertTrue(StoB(status))

        status = ShoppingPolicyLogic.add_shopping_policy_on_items('Ultimate_ShaharShahar', "", "", "N", 0)
        self.assertTrue(StoB(status))

        IP = ShoppingPolicyLogic.get_all_shopping_policy_on_identity()
        CP = ShoppingPolicyLogic.get_all_shopping_policy_on_category()
        ITP = ShoppingPolicyLogic.get_all_shopping_policy_on_items()
        SP = ShoppingPolicyLogic.get_all_shopping_policy_on_shop('eBay')
        self.assertEqual(len(IP), 2)
        self.assertEqual(len(CP), 2)
        self.assertEqual(len(ITP), 2)
        self.assertEqual(len(SP), 2)

    def test_update_policy(self):
        status = True
        status &= StoB(ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'eBay', "", "N", 0))
        status &= StoB(ShoppingPolicyLogic.add_shopping_policy_on_identity('Ultimate_ShaharShahar', "", "N", 0))
        status &= StoB(ShoppingPolicyLogic.add_shopping_policy_on_category('Ultimate_ShaharShahar', "", "", "N", 0))
        status &= StoB(ShoppingPolicyLogic.add_shopping_policy_on_items('Ultimate_ShaharShahar', "", "", "N", 0))

        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_shop('ShaharBenS2', 1, "restriction", "N", 'eBay'))
        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_shop('ShaharBenS2', 1, "quantity", 10, 'eBay'))

        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_identity('Ultimate_ShaharShahar', 1, "restriction", "AL"))
        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_identity('Ultimate_ShaharShahar', 1, "quantity", 4))

        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_category('Ultimate_ShaharShahar', 1, "restriction", "E"))
        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_category('Ultimate_ShaharShahar', 1, "quantity", 3))
        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_category('Ultimate_ShaharShahar', 1, "category", "books"))

        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_items('Ultimate_ShaharShahar', 1, "restriction", "UT"))
        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_items('Ultimate_ShaharShahar', 1, "quantity", 10))
        status &= StoB(
            ShoppingPolicyLogic.update_shopping_policy_on_items('Ultimate_ShaharShahar', 1, "item_name", "DP by GoF"))
        self.assertTrue(status)

        IP = ShoppingPolicyLogic.get_all_shopping_policy_on_identity()
        CP = ShoppingPolicyLogic.get_all_shopping_policy_on_category()
        ITP = ShoppingPolicyLogic.get_all_shopping_policy_on_items()
        SP = ShoppingPolicyLogic.get_all_shopping_policy_on_shop('eBay')

        self.assertEqual(IP[0].restriction, "AL")
        self.assertEqual(IP[0].quantity, 4)

        self.assertEqual(CP[0].restriction, "E")
        self.assertEqual(CP[0].quantity, 3)
        self.assertEqual(CP[0].category, "books")

        self.assertEqual(ITP[0].restriction, "UT")
        self.assertEqual(ITP[0].quantity, 10)
        self.assertEqual(ITP[0].item_name, "DP by GoF")

        self.assertEqual(SP[0].restriction, "N")
        self.assertEqual(SP[0].quantity, 10)

    # def test_remove_policy(self):
    #    pass

    def test_condition_syntax(self):
        ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'eBay', "", "N", 0)
        ShoppingPolicyLogic.add_shopping_policy_on_identity('Ultimate_ShaharShahar', "", "N", 0)
        ShoppingPolicyLogic.add_shopping_policy_on_category('Ultimate_ShaharShahar', "", "", "N", 0)
        ShoppingPolicyLogic.add_shopping_policy_on_items('Ultimate_ShaharShahar', "", "", "N", 0)

        status = True
        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_shop('ShaharBenS2', 1, 'conditions',
                                                                          "age > 18 AND sex = ''Male''", 'eBay'))
        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_items('Ultimate_ShaharShahar', 1, 'conditions',
                                                                           "state = ''AFG'' AND sex = ''Male''"))
        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_category('Ultimate_ShaharShahar', 1, 'conditions',
                                                                              "(age > 18 AND sex = ''Male'') OR (NOT state != ''ZMB'')",
                                                                              ))
        status &= StoB(ShoppingPolicyLogic.update_shopping_policy_on_identity('Ultimate_ShaharShahar', 1, 'conditions',
                                                                              "NOT sex != ''Female''"))

        self.assertTrue(status)

    def test_condition_bad_syntax(self):
        ShoppingPolicyLogic.add_shopping_policy_on_shop('ShaharBenS2', 'eBay', "", "N", 0)
        ShoppingPolicyLogic.add_shopping_policy_on_identity('Ultimate_ShaharShahar', "", "N", 0)
        ShoppingPolicyLogic.add_shopping_policy_on_category('Ultimate_ShaharShahar', "", "", "N", 0)
        ShoppingPolicyLogic.add_shopping_policy_on_items('Ultimate_ShaharShahar', "", "", "N", 0)

        status = StoB(ShoppingPolicyLogic.update_shopping_policy_on_shop('ShaharBenS2', 1, 'conditions',
                                                                         "age >> 18 AND sex = ''Male''", 'eBay'))
        self.assertFalse(status)
        status = StoB(ShoppingPolicyLogic.update_shopping_policy_on_items('Ultimate_ShaharShahar', 1, 'conditions',
                                                                          "state1 = ''AFG'' AND sex = ''Male''"))
        self.assertFalse(status)

        status = StoB(ShoppingPolicyLogic.update_shopping_policy_on_category('Ultimate_ShaharShahar', 1, 'conditions',
                                                                             "(age > 18 AND sex = ''Male'') OR (NOT state != ''ZMBZA'')",
                                                                             ))
        self.assertFalse(status)

        status = StoB(ShoppingPolicyLogic.update_shopping_policy_on_identity('Ultimate_ShaharShahar', 1, 'conditions',
                                                                             "NOT sex != ''Female'' (DELETE * FROM *)"))
        self.assertFalse(status)

    def test_policy_logic(self):
        pass

    def test_policy_logic_bad(self):
        pass

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
