from django.urls import path
from . import views


app_name = "auction"
urlpatterns = [
    path("", views.home, name="home"),
    path("lot/bid/<uuid:lot_id>/", views.lot_bid_view, name="lot_bid_view"),
    path("cart/", views.cart_view, name="cart_details"),
    path("checkout/", views.checkout, name="checkout"),
    path("toggle-user-as-marketer",
        views.toggle_user_as_marketer,
        name="toggle_user_as_marketer"),
    path("auction/", views.add_auction, name="add_auction"),
    path('mark_lot_as_paid/', views.mark_lot_as_paid, name='mark_lot_as_paid'),
    
    # API endpoints
    
    path("has-expired/<uuid:lot_id>/",
         views.get_lot_has_endtime, name="lot_has_expired"),
    path("mark-lot-as-sold/<uuid:lot_id>/",
         views.mark_lot_as_sold, name="mark_lot_as_sold"),
    path("get-lot-price/<uuid:lot_id>/",
         views.get_lot_price, name="get_lot_price"),
]
