from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm


app_name = "account"
urlpatterns = [
	path("", views.signup, name="signup"),
	path("signin/",
		auth_views.LoginView.as_view(
			template_name="account/signin.html",
			authentication_form=LoginForm
		),
		name="signin"
	),
]