from locust import HttpLocust, TaskSet, task
from http import cookiejar, cookies

# Can support 200 users 0% FAIL

user_num = 1


def update():
    global user_num
    user_num += 1


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """

        self.has_store = False
        self.item_counter = 0
        self.num = user_num
        update()

        self.register()
        self.login()
        # self.create_shop()

    def register(self):
        self.client.post("app/users/register/",
                         {"username": "user" + str(self.num) + "user", "password": "12345678", "state": "AFG",
                          "sex": "Female", "age": 12})

    def login(self):
        response = self.client.post("app/users/login/",
                                    {"username": "user" + str(self.num) + "user", "password": "12345678"})

        # cookie = cookiejar.Cookie(0, "login_hash", response.content, 8000, True, "localhost", True, False, "/", True,
        #                          False, 1592296482, False, "testing", None, None, False)

        # self.cookies = cookiejar.CookieJar()
        # self.cookies.set_cookie(cookie)
        self.login_hash = response.content.decode("utf-8")
        # print(str(self.login_hash))

    @task(20)
    def index(self):
        self.client.get("app/home/")

    @task(10)
    def profile(self):
        self.client.get("app/my/account/?login_hash=" + self.login_hash)

    @task(3)
    def create_shop(self):
        if self.has_store is False:
            self.client.post("app/shops/create_shop/",
                             {"name": "shop" + str(self.num), "status": "Inactive", "login_hash": self.login_hash})
            self.has_store = True

    @task(3)
    def add_item(self):
        if self.has_store:
            self.client.post("app/items/add_item_to_shop/", {
                "shop_name": "shop" + str(self.num),
                "item_name": "coolItem" + str(self.num) + str(self.item_counter),
                "item_quantity": self.num,
                "item_category": str(self.num) + "_items",
                "item_keywords": "testing",
                "item_price": self.num * 3,
                "item_url": "https://53744bf91d44b81762e0-fbbc959d4e21c00b07dbe9c75f9c0b63.ssl.cf3.rackcdn.com/media/D8/D8FDF3A5-A81A-47FA-8382-7C54BF3FEAF6/Presentation.Large/Mountain-chicken-side-view.jpg",
                "item_kind": "regular",
                "login_hash": self.login_hash
            })
            self.item_counter += 1


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 500
