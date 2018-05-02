from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from ServiceLayer import Consumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([url(r"^test/", Consumer.Consumer)]),
})
