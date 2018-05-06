import os
import unittest

from DatabaseLayer.initializeDatabase import init_database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FirstTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_register(self):
        self.driver = webdriver.Chrome("C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get("http://www.google.com")

    def test_facebook(self):
        user = "yonits12@gmail.com"
        pwd = "999150508"
        self.driver = webdriver.Chrome("C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://www.facebook.com")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("email")
        elem.send_keys(user)
        elem = self.driver.find_element_by_id("pass")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        self.driver.close()

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
