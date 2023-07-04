# django imports
from django.shortcuts import render, redirect
from django.contrib import messages
from email_verification.views import VerifyEmail

# custom imports
from .forms import UserRegistrationForm


def signup(request):
    form = UserRegistrationForm()

    # post request handler
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            VerifyEmail(request, form)
            
            # send success message
            messages.success(request, "Complete your registration from your email")
            
            # redirect to login
            return redirect("account:signin")

    return render(request, "account/signup.html", {"form": form})
