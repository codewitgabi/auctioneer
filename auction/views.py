import json
from uuid import uuid4

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models  import Group, Permission
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Lot, Bid, LotImage


User = get_user_model()


@login_required
def home(request: HttpRequest):
    """
    Auctioneer Home Page
    """
    # set session expiry to four days
    request.session.set_expiry(24 * 4 * 60 * 60)
    lots = Lot.objects.filter(sold=False)[:20]
    
    context: dict = {
        "lots": lots,
    }
    return render(request, "auction/home.html", context)


@login_required
def lot_bid_view(request: HttpRequest, lot_id: uuid4):
    """
    Diplays the lot detail in full and shows bidding detail.
    Users can also place their bids here and see the bids of other users in realtime.
    """
    lot = get_object_or_404(Lot, id=lot_id)

    if not lot.is_ready:
        return redirect("auction:home")

    _ = Bid.objects.get_or_create(bidder=request.user, lot=lot)[0]
    # Check if the lot is paid
    is_paid = lot.paid

    context: dict = {"lot": lot, "is_paid": is_paid}
    return render(request, "auction/lot-detail.html", context)

@login_required
def paid_lots_view(request):
    paid_lots = Lot.objects.filter(paid=True)
    return render(request, 'paid_lots.html', {'lots': paid_lots})

@login_required
def unpaid_lots_view(request):
    unpaid_lots = Lot.objects.filter(paid=False)
    return render(request, 'unpaid_lots.html', {'lots': unpaid_lots})
    
@login_required
def cart_view(request: HttpRequest):
    """
    Displays all lots won by the current logged in user where they can proceed to the checkout for payment.
    """
    context: dict = {}
    return render(request, "auction/cart.html", context)
    
    
@login_required
def checkout(request: HttpRequest):
    """
    View to make payment
    """
    
    context: dict = {
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID,
    }
    return render(request, "auction/checkout.html", context)


@api_view(["GET"])
def get_lot_has_endtime(request: HttpRequest, lot_id: uuid4):
    """
    Checks if a lot has ended
    """
    # get lot object
    lot = get_object_or_404(Lot, id=lot_id)

    return Response({
        "has_ended": lot.has_ended}, status=status.HTTP_200_OK)


@api_view(["GET"])
def mark_lot_as_sold(request: HttpRequest, lot_id: uuid4):
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
def get_lot_price(request: HttpRequest, lot_id: uuid4):
    """
    Returns the lot price of a given lot.
    Used for updating the frontend lotPrice so that the lotPrice is set globally for all users bidding for the lot with the given lot_id
    """
    # get lot object
    lot = get_object_or_404(Lot, id=lot_id)

    return Response({"lot_price": float(lot.price)}, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_payment(request: HttpRequest):
    """
    Verifies payment
    """
    data = json.loads(request.body)
    lot_id = data.get("lot_id")
    lot = get_object_or_404(Lot, id=lot_id)
    lot.paid = True
    lot.save()
    return Response({"message": "Payment verified and lot marked as paid."}, status=status.HTTP_200_OK)
    
    pass


@login_required
def toggle_user_as_marketer(request: HttpRequest):
    """
    Add user to marketers `Group`
    """
    user = request.user
    permission: Permission = Permission.objects.get(codename="add_lot")
    group = Group.objects.get_or_create(name="Marketers")[0]
    group.permissions.add(permission.id)
    group.save()
    
    if user.groups.filter(name=group).exists():
        user.groups.remove(group)
    else:
        user.groups.add(group)
    user.save()
    
    return redirect("auction:home")


@login_required
@permission_required("auction.add_lot", raise_exception=True)
def add_auction(request: HttpRequest):
    context: dict = {}
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        start_date = request.POST.get("auction_date")
        endtime = request.POST.get("endtime")
        price = request.POST.get("price")
        increment = request.POST.get("increment")
        
        newLot: Lot = Lot.objects.create(
            name=name,
            description=description,
            price=price,
            increment=increment,
            endtime=endtime,
            auction_date=start_date
        )
        
        lot_images: list = request.FILES.getlist("lot_images")
        for image in lot_images:
            LotImage.objects.create(image=image, lot=newLot)
        
        return redirect("auction:add_auction")
    return render(request, "auction/add_lot.html", context)
