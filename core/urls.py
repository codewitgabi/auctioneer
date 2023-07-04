from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from account.forms import ResetPasswordForm, SetNewPasswordForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("account.urls")),
    path("", include("auction.urls")),
    path("password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name= "account/password-reset.html",
            form_class=ResetPasswordForm
        ),
        name= "password_reset"
    ),
    path("passwordreset-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name= "account/password-reset-done.html"
        ),
        name= "password_reset_done"
    ),
    path("password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name= "account/password-reset-confirm.html",
            form_class=SetNewPasswordForm
        ),
        name= "password_reset_confirm"
    ),
    path("password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name= "account/password-reset-complete.html"
        ),
        name= "password_reset_complete"
    ),
]

