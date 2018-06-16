from random import randint

from locust import HttpLocust, TaskSet, task
from http import cookiejar, cookies

# Can support 100 users 4% FAIL


user_num = 1


def update():
    global user_num
    user_num += 1


item_id = -1


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        global item_id
        self.num = user_num
        update()

        self.register()
        self.login()
        if self.num == 1:
            # Master
            for i in range(3):
                self.create_shop(i)
                for j in range(10):
                    self.add_item(i, j)
            response = self.client.get("app/items/get_id_by_name/?item_name=coolItem00", )
            item_id = response.content.decode("utf-8")

    def register(self):
        self.client.post("app/users/register/",
                         {"username": "user" + str(self.num) + "user", "password": "12345678", "state": "AFG",
                          "sex": "Female", "age": 12})

    def login(self):
        response = self.client.post("app/users/login/",
                                    {"username": "user" + str(self.num) + "user", "password": "12345678"})

        self.login_hash = response.content.decode("utf-8")

    def create_shop(self, i):
        self.client.post("app/shops/create_shop/",
                         {"name": "shop" + str(i), "status": "Inactive", "login_hash": self.login_hash})

    def add_item(self, shop_id, id):
        self.client.post("app/items/add_item_to_shop/", {
            "shop_name": "shop" + str(shop_id),
            "item_name": "coolItem" + str(shop_id) + str(id),
            "item_quantity": 100,
            "item_category": str(shop_id) + "_items",
            "item_keywords": "testing",
            "item_price": 100 + 100 * shop_id,
            "item_url": "https://53744bf91d44b81762e0-fbbc959d4e21c00b07dbe9c75f9c0b63.ssl.cf3.rackcdn.com/media/D8/D8FDF3A5-A81A-47FA-8382-7C54BF3FEAF6/Presentation.Large/Mountain-chicken-side-view.jpg",
            "item_kind": "regular",
            "login_hash": self.login_hash
        })

    @task(10)
    def add_to_cart(self):
        if int(item_id) >= 0 and self.num != 1:
            self.client.post("app/shopping_cart/add_item_shopping_cart/", {
                "item_id": randint(int(item_id), int(item_id) + 30),
                "quantity": 5,
                'login_hash': self.login_hash
            })

    @task(1)
    def pay_all(self):
        if int(item_id) >= 0 and self.num != 1:
            self.client.post("app/shopping_cart/pay_all/", {
                'login_hash': self.login_hash
            })


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 500
