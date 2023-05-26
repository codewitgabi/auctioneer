from django.urls import path
from . import views


app_name = "auction"
urlpatterns = [
	path("", views.home, name="home"),
	path("lot/bid/<uuid:lot_id>/", views.lot_bid_view, name="lot_bid_view"),
]