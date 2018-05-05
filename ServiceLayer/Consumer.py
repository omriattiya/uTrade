'''
from channels.generic.websocket import WebsocketConsumer
import threading

connectedUsers = {}
connectedConsumers = {}

loggedInUsers = {}
event = threading.Event()
alerts_queue = []
user_alerts_box = {}


def notify_live_alerts(users, msg):
    alerts_queue.append({'users': users, 'msg': msg})
    event.set()


def live_alerts():
    while True:
        event.wait()
        # if here than there are probably live alerts to send
        for alert in alerts_queue:
            users = alert.get('users')
            for user in users:
                connected_user = connectedUsers.get(user)
                if connected_user is not None:
                    user_box = user_alerts_box.get(user)
                    if user_box is None:
                        user_alerts_box[user] = []
                    user_box = user_alerts_box.get(user)
                    user_box.append(alert.get('msg'))
                    connected_user.send_alert_count(len(user_box))
            alerts_queue.remove(alert)

        event.clear()


try:
    live_alerts_thread = threading.Thread(None, live_alerts, "Live_Alerts")
    live_alerts_thread.start()
except:
    print("Can't start live alerts thread")


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

    def send_alert_count(self,count):
        self.send(str(count))

    def disconnect(self, message):
        username = connectedConsumers.get(self)
        if username is not None:
            del connectedConsumers[self]
            del connectedUsers[username]
'''