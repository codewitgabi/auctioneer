import os
from threading import Thread
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from email_verification.views import delete_inactive_users

import auction.routers
from auction.utils import ensure_lot_winner

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')


application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(
				auction.routers.websocket_urlpatterns,
			)
		)
	)
})

t = Thread(target=ensure_lot_winner)
t.start()

email_thread = Thread(target=delete_inactive_users)
email_thread.start()