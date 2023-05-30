from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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

