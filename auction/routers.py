from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
	re_path(r"^bid/(?P<lot_id>[0-9a-f-]+)/$", consumers.BidConsumer.as_asgi()),
]