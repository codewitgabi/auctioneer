import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Lot, Bid


@login_required
def home(request):
    """
    Auctioneer Home Page
    """
    # set session expiry to four days
    request.session.set_expiry(24 * 4 * 60 * 60)
    lots = Lot.objects.filter(sold=False)[:20]
    context: dict = {
        "lots": lots
    }
    return render(request, "auction/home.html", context)


@login_required
def lot_bid_view(request, lot_id):
    """
    Diplays the lot detail in full and shows bidding detail.
    Users can also place their bids here and see the bids of other users in realtime.
    """
    lot = get_object_or_404(Lot, id=lot_id)

    if not lot.is_ready:
        return redirect("auction:home")

    _ = Bid.objects.get_or_create(bidder=request.user, lot=lot)[0]

    context: dict = {"lot": lot}
    return render(request, "auction/lot-detail.html", context)


@login_required
def cart_view(request):
    """
    Displays all lots won by the current logged in user where they can proceed to the checkout for payment.
    """
    context: dict = {}
    return render(request, "auction/cart.html", context)
    
    
@login_required
def checkout(request):
    """
    View to make payment
    """
    
    context: dict = {
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID,
    }
    return render(request, "auction/checkout.html", context)


@api_view(["GET"])
def get_lot_has_endtime(request, lot_id):
    """
    Checks if a lot has ended
    """
    # get lot object
    lot = get_object_or_404(Lot, id=lot_id)

    return Response({
        "has_ended": lot.has_ended}, status=status.HTTP_200_OK)


@api_view(["GET"])
def mark_lot_as_sold(request, lot_id):
    """
    Marks a lot with the specified lot_id as sold and also mark the buyer of the lot as the highest bidder of that lot.
    """
    # get lot object
    lot = get_object_or_404(Lot, id=lot_id)
    lot.buyer = lot.bid_set.order_by("-bid").first().bidder
    lot.sold = True
    lot.save()

    return Response({"status": "success"}, status=status.HTTP_205_RESET_CONTENT)


@api_view(["GET"])
def get_lot_price(request, lot_id):
    """
    Returns the lot price of a given lot.
    Used for updating the frontend lotPrice so that the lotPrice is set globally for all users bidding for the lot with the given lot_id
    """
    # get lot object
    lot = get_object_or_404(Lot, id=lot_id)

    return Response({"lot_price": float(lot.price)}, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_payment(request):
    """
    Verifies payment
    """
    data = json.loads(request.body)
    
    pass