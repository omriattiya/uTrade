import unittest

# import your test modules
from Tests.UnitTests import SearchTests, ShopTests, MessagesTests, UsersTest, OwnerTests, ItemsTests, ShoppingCartTests, \
    StoreManagersTests, ShoppingTests, AuctionTests, LotteryTests

if __name__ == "__main__":
    # initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(AuctionTests))
    suite.addTests(loader.loadTestsFromModule(ItemsTests))
    suite.addTests(loader.loadTestsFromModule(LotteryTests))
    suite.addTests(loader.loadTestsFromModule(MessagesTests))
    suite.addTests(loader.loadTestsFromModule(OwnerTests))
    suite.addTests(loader.loadTestsFromModule(SearchTests))
    suite.addTests(loader.loadTestsFromModule(ShoppingCartTests))
    suite.addTests(loader.loadTestsFromModule(ShoppingTests))
    suite.addTests(loader.loadTestsFromModule(ShopTests))
    suite.addTests(loader.loadTestsFromModule(StoreManagersTests))
    suite.addTests(loader.loadTestsFromModule(UsersTest))

    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)