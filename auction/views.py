from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Lot, Bid


@login_required
def home(request):
	lots = Lot.objects.all()
	context: dict = {
		"lots": lots
	}
	return render(request, "auction/home.html", context)


@login_required
def lot_bid_view(request, lot_id):
	lot = get_object_or_404(Lot, id=lot_id)
	
	if not lot.is_ready:
		return redirect("auction:home")
		
	_ = Bid.objects.get_or_create(bidder=request.user, lot=lot)[0]
	
	context: dict = {"lot": lot}
	return render(request, "auction/lot-detail.html", context)


@api_view(["GET"])
def get_lot_has_endtime(request, lot_id):
	# get lot object
	lot = get_object_or_404(Lot, id=lot_id)
	
	return Response({
		"has_ended": lot.has_ended}, status=status.HTTP_200_OK)

