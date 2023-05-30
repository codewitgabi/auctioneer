from django.urls import path
from . import views


app_name = "auction"
urlpatterns = [
	path("", views.home, name="home"),
	path("lot/bid/<uuid:lot_id>/", views.lot_bid_view, name="lot_bid_view"),
	path("has-expired/<uuid:lot_id>/", views.get_lot_has_endtime, name="lot_has_expired"),
	path("mark-lot-as-sold/<uuid:lot_id>/", views.mark_lot_as_sold, name="mark_lot_as_sold"),
]