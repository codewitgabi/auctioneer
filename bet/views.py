# django imports
from django.shortcuts import render, redirect
from django.contrib import messages

# custom imports
from .forms import UserRegistrationForm


def signup(request):
	form = UserRegistrationForm()
	
	# post request handler
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("bet:signin")
	
	return render(request, "bet/signup.html", {"form": form})
