from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from ServiceLayer.services.LiveAlerts import Consumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([url(r"^live_alerts/$", Consumer.Consumer)]),
})
