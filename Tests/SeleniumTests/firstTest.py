import os
import unittest

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from DatabaseLayer.initializeDatabase import init_database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from DomainLayer import UsersLogic
from SharedClasses.RegisteredUser import RegisteredUser


class FirstTest(unittest.TestCase):
    def setUp(self):
        init_database('db.sqlite3')

    def test_register(self):
        self.driver = webdriver.Chrome("C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get("http://www.google.com")

    def test_register(self):
        user = "NadavGeverAl"
        pwd = "123456789"
        self.driver = webdriver.Chrome("C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        self.driver.close()

    def test_Login(self):
        user = "NadavKing"
        pwd = "123456789"
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 5)
        try:
            page_loaded = wait.until(lambda browser: "y" == "u")
        except TimeoutException:
            self.driver.get("http://localhost:8000/app/home/")
            # assert "Facebook" in self.driver.title
            elem = self.driver.find_element_by_id("login_elem")
            elem.click()
            wait = WebDriverWait(self.driver, 5)
            try:
                page_loaded = wait.until(lambda browser: "y" == "u")
            except TimeoutException:
                elem = self.driver.find_element_by_id("email-modal")
                elem.send_keys(user)
                elem = self.driver.find_element_by_id("password-modal")
                elem.send_keys(pwd)
                elem.send_keys(Keys.RETURN)
                wait = WebDriverWait(self.driver, 5)
                try:
                    page_loaded = wait.until(lambda browser: "y" == "u")
                except TimeoutException:
                    self.driver.close()

    def test_Bad_Login(self):
        user = "NadavSuperman"
        pwd = "123456789"
        pwd_wrong = "123465789"
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd)
        wait = WebDriverWait(self.driver, 1)
        try:
            page_loaded = wait.until(lambda browser: "y" == "u")
        except TimeoutException:
            elem.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 3)
        try:
            page_loaded = wait.until(lambda browser: "y" == "u")
        except TimeoutException:
            self.driver.get("http://localhost:8000/app/home/")
            # assert "Facebook" in self.driver.title
            elem = self.driver.find_element_by_id("login_elem")
            elem.click()
            wait = WebDriverWait(self.driver, 2)
            try:
                page_loaded = wait.until(lambda browser: "y" == "u")
            except TimeoutException:
                elem = self.driver.find_element_by_id("email-modal")
                elem.send_keys(user)
                elem = self.driver.find_element_by_id("password-modal")
                elem.send_keys(pwd_wrong)
                wait = WebDriverWait(self.driver, 2)
                try:
                    page_loaded = wait.until(lambda browser: "y" == "u")
                except TimeoutException:
                    elem.send_keys(Keys.RETURN)
                    wait = WebDriverWait(self.driver, 3)
                    try:
                        page_loaded = wait.until(lambda browser: "y" == "u")
                    except TimeoutException:
                        self.driver.close()

    def test_Bad_Registration(self):
        user = "NadavTheBest"
        pwd_wrong = "1234567$"
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd_wrong)
        wait = WebDriverWait(self.driver, 1)
        try:
            page_loaded = wait.until(lambda browser: "y" == "u")
        except TimeoutException:
            elem.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 3)
        try:
            page_loaded = wait.until(lambda browser: "y" == "u")
        except TimeoutException:
            self.driver.close()

    def tearDown(self):
        os.remove('db.sqlite3')


if __name__ == '__main__':
    unittest.main()
