import os
import unittest
from DatabaseLayer.getConn import delete_content
from ServiceLayer.services.LiveAlerts import Consumer

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class GUI_Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_delete_all(self):
        delete_content()
        Consumer.loggedInUsers = {}
        Consumer.loggedInUsersShoppingCart = {}
        Consumer.connectedUsers = {}
        Consumer.connectedConsumers = {}
        Consumer.guestShoppingCart = {}
        Consumer.guestIndex = 0
        Consumer.user_alerts_box = {}
        self.assertTrue(True)

    def test_aaa_register(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        alert_text = ""
        self.driver = webdriver.Chrome("C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("state")
        elem.send_keys("ZMB")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("age")
        elem.send_keys("34")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("sex")
        elem.send_keys("Male")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("register_submit")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "User added successfully")

    def test__aa_bad_pass_Registration(self):
        user = "NadavTheBest"
        pwd_wrong = "1234567$"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd_wrong)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("state")
        elem.send_keys("ZMB")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("age")
        elem.send_keys("34")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("sex")
        elem.send_keys("Male")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("register_submit")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "FAILED: Password must be 8 to 20 alphabetic letters and numbers")

    def test__ab_bad_user_Registration(self):
        user = "nadav space"
        pwd_wrong = "12345678"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home/register/")
        # assert "Facebook" in self.driver.title
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(pwd_wrong)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("state")
        elem.send_keys("ZMB")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("age")
        elem.send_keys("34")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("sex")
        elem.send_keys("Male")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("register_submit")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "FAILED: Username must be 8 to 20 alphabetic letters and numbers")

    def test_ac_Login_Bad_pass(self):
        user = "NadavGeverAl"
        wrong_pwd = "123456789"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        # assert "Facebook" in self.driver.title
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(wrong_pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "FAILED:Password in incorrect")

    def test_ad_Login_bad_username(self):
        user = "NadavGeverGever"
        wrong_pwd = "123456789"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        # assert "Facebook" in self.driver.title
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(wrong_pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "FAILED: Username is incorrect")

    def test_ae_Login(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        # assert "Facebook" in self.driver.title
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 4)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.driver.quit()
        self.assertEqual(logged_user, "NadavGeverAl")

    def test_af_Logout(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 4)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        # _____ end login _____
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Private_Area")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Logout")
        elem.click()
        wait_for(self, 3)
        elem = self.driver.find_element_by_id("login_element")
        login_label = elem.text
        self.driver.quit()
        self.assertEqual(login_label, "Login")

    def test_ag_Login_and_create_shop(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        shop_name = "Vol(G)och"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        # assert "Facebook" in self.driver.title
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 4)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        # ______ create the shop _______
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Private_Area")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("my_shops")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("create_shop")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("shop-name-modal")
        elem.send_keys(shop_name)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("create_shop_btn")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "Your shop has been opened!")

    def test_ag_Activate_shop_and_hire_owner_bad(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 4)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        # _____ end login _____
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Private_Area")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("my_shops")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Vol(G)och_status")
        self.assertEqual(elem.text, "Inactive")
        elem.click()
        wait_for(self, 2)
        elem = self.driver.find_element_by_id("Vol(G)och_status")
        self.assertEqual(elem.text, "Active")
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("addOwnerOpened")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("owner-name-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Add_Owner_submit")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "FAILED! NadavGeverAl is already an owner")

    def test_ah_Add_item_and_purchase_policy(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        Name = "milk"
        Quantity = "650"
        Category = "Dairy"
        KeyWords = "tara"
        Price = "4"
        URL = "https://cdn.motherandbaby.co.uk/web/1/root/shutterstock-269001833_w555.jpg"
        Kind = "regular"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 4)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        # _____ end login _____
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Private_Area")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("my_shops")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("enter_to_shop")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("add_item")
        elem.click()
        wait_for(self, 1)
        # ______ Add Item ______
        elem = self.driver.find_element_by_id("name")
        elem.send_keys(Name)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("quantity")
        elem.send_keys(Quantity)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("category")
        elem.send_keys(Category)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("keywords")
        elem.send_keys(KeyWords)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("price")
        elem.send_keys(Price)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("url")
        elem.send_keys(URL)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("kind")
        elem.send_keys(Kind)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("Add_item_submit")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "Item Added Successfully")

    def test_ai_Add_discount(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        percent = "20"
        duration = "22/03/2019"
        kind = "Visible - Item"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 2)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        # _____ end login _____
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("Private_Area")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("my_shops")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("enter_to_shop")
        elem.click()
        wait_for(self, 1)
        # ______ Find ID ______
        elem = self.driver.find_element_by_id("edit_remove")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("item_id_id")
        item_id = elem.text[9:10]
        elem = self.driver.find_element_by_id("parent_shop")
        elem.click()
        wait_for(self, 1)
        # ______ Add Discount ______
        elem = self.driver.find_element_by_id("add_discount")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("item_id")
        elem.send_keys(item_id)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("percent")
        elem.send_keys(percent)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("duration")
        elem.send_keys(duration)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("kind")
        elem.send_keys(kind)
        elem = self.driver.find_element_by_id("item_id")
        elem.send_keys(item_id)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("add_discount_submit")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 2)
        self.driver.quit()
        self.assertEqual(alert_text, "Discount Added Successfully")

    def test_aj_BUY_ITEM(self):
        user = "NadavGeverAl"
        pwd = "12345678"
        Firstname = "Nadav"
        Lastname = "Hashpitz"
        Company = "BGU"
        Address = "SadnaStreet"
        Telephone = "0512346789"
        Email= "voloch@post.bgu.ac.il"
        alert_text = ""
        self.driver = webdriver.Chrome(
            "C:/Users/Yoni/Desktop/Installations of Applications/chromedriver_win32/chromedriver.exe")
        self.driver.get("http://localhost:8000/app/home")
        elem = self.driver.find_element_by_id("login_element")
        elem.click()
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("email-modal")
        elem.send_keys(user)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("password-modal")
        elem.send_keys(pwd)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("login_btn")
        elem.click()
        wait_for(self, 2)
        elem = self.driver.find_element_by_id("strong_username")
        logged_user = elem.text
        self.assertEqual(logged_user, "NadavGeverAl")
        # _____ end login _____
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("enter_item_page")
        elem.click()
        wait_for(self, 1)
        # ______ Find ID ______
        elem = self.driver.find_element_by_id("quantity_input")
        elem.send_keys("5")
        elem = self.driver.find_element_by_id("add_to_cart_btn")
        elem.click()
        wait_for(self, 1)
        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present(),
                                                'Waiting for alert timed out')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
        wait_for(self, 1)
        self.assertEqual(alert_text, "add to cart success")
        elem = self.driver.find_element_by_id("goto_shopping_cart")
        elem.click()
        wait_for(self, 1)
        # ______ Inside Shop Cart ______
        elem = self.driver.find_element_by_id("proceed")
        elem.click()
        wait_for(self, 1)

        elem = self.driver.find_element_by_id("firstname")
        elem.send_keys(Firstname)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("lastname")
        elem.send_keys(Lastname)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("company")
        elem.send_keys(Company)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("street")
        elem.send_keys(Address)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("phone")
        elem.send_keys(Telephone)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("email")
        elem.send_keys(Email)
        wait_for(self, 0.5)
        elem = self.driver.find_element_by_id("continue")
        elem.click()
        wait_for(self, 1)
        elem = self.driver.find_element_by_id("place_an_order")
        elem.click()
        wait_for(self, 2)
        elem = self.driver.find_element_by_id("confirm")
        self.assertEqual(elem.text, "Order Confirmation")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()


def wait_for(self, time):
    wait = WebDriverWait(self.driver, 2)
    try:
        page_loaded = wait.until(lambda browser: "y" == "u")
    except TimeoutException:
        return
