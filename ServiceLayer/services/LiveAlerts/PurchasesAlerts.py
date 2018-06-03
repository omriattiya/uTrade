import threading
from ServiceLayer.services.LiveAlerts import Consumer
from ServiceLayer.services.LiveAlerts.Messages.Purchasing import PurchasingMessage

event = threading.Event()

purchases_alerts_queue = []


def notify_purchasing_alerts(users, msg):
    purchases_alerts_queue.append({'users': users, 'msg': PurchasingMessage(msg)})
    event.set()


def messaging_live_alerts():
    while True:
        event.wait()
        # if here than there are probably live alerts to send
        for alert in purchases_alerts_queue:
            users = alert.get('users')
            for user in users:
                #connected_user = Consumer.connectedUsers.get(user)
                #if connected_user is not None:
                user_box = Consumer.user_alerts_box.get(user)
                if user_box is None:
                    Consumer.user_alerts_box[user] = []
                user_box = Consumer.user_alerts_box.get(user)
                user_box.append(alert.get('msg'))
                connected_user = Consumer.connectedUsers.get(user)
                if connected_user is not None:
                    connected_user.send_alert_count(len(user_box))
            purchases_alerts_queue.remove(alert)

        event.clear()


def init_thread():
    try:
        live_alerts_thread = threading.Thread(None, messaging_live_alerts, "Purchasing_Live_Alerts")
        live_alerts_thread.start()
    except:
        print("Can't start purchasing alerts thread")
