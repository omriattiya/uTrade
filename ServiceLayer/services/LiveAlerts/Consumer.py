#from channels.generic.websocket import WebsocketConsumer
from ServiceLayer.services.LiveAlerts import MessagingAlerts, PurchasesAlerts, LoterryAlerts

loggedInUsers = {}
loggedInUsersShoppingCart = {}

connectedUsers = {}
connectedConsumers = {}


guestShoppingCart = {}
guestIndex = 0
user_alerts_box = {}


MessagingAlerts.init_thread()
PurchasesAlerts.init_thread()
LoterryAlerts.init_thread()

'''
class Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, *, text_data):
        username = loggedInUsers.get(text_data)
        if username is not None:
            connectedUsers[username] = self
            connectedConsumers[self] = username
            alert_box = user_alerts_box.get(username)
            if alert_box is not None:
                self.send(str(len(alert_box)))

    def send_alert_count(self, count):
        self.send(str(count))

    def disconnect(self, message):
        username = connectedConsumers.get(self)
        if username is not None:
            del connectedConsumers[self]
            del connectedUsers[username]

'''