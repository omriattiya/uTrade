from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

import TestConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([url(r"^test/", TestConsumer.TestConsumer)]),
})
