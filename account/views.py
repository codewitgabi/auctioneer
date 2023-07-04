# django imports
from django.shortcuts import render, redirect
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

    return render(request, "account/signup.html", {"form": form})
