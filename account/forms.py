# django imports
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

# user object
User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    Custom User Registration Form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password2"].required = False
        
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            "name": "email",
            "type": "email",
            "id": "email",
            "placeholder": "Email"
        })
    )

    username = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            "name": "username",
            "id": "username",
            "placeholder": "Username",
        })
    )

    password1 = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "name": "password",
            "id": "password",
            "placeholder": "Password"
        })
    )

    class Meta:
        model = User
        fields = ("email", "username", "password1")

    def clean_password1(self, *args, **kwargs):
        symbols = "@#_~[]{}()$&?%/"
        password = self.cleaned_data.get("password1")

        # MinimumLengthValidator
        if len(password) < 10:
            raise forms.ValidationError(
                "Password is too short. Requires a minimum of 10 characters")

        # CommonPasswordValidator
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError("Password is too common.")

        # NoSymbolValidator
        if not any([sym in symbols for sym in password]):
            raise forms.ValidationError(
                f"Password should contain any of {symbols}")

        return password


class LoginForm(AuthenticationForm):
    """ Custom Authentication/Login form """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs.update({
            "placeholder": "Password",
            "id": "password",
            "name": "password"
        })
        
    username = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            "type": "email",
            "name": "email",
            "id": "email",
            "placeholder": "Email",
        })
    )

    class Meta:
        model = User
        fields = ("username", "password")


class ResetPasswordForm(PasswordResetForm):
    """ Custom PasswordResetForm """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            "name": "email",
            "type": "email",
            "id": "email",
            "placeholder": "Email"
        })
    )
    
    class Meta:
        model = User
        fields = ("email",)


class SetNewPasswordForm(SetPasswordForm):
    """ Custom SetPasswordForm """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    new_password1 = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "name": "new_password1",
            "placeholder": "Password"
        })
    )
    
    new_password2 = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(attrs={
            "type": "password",
            "name": "new_password2",
            "placeholder": "Confirm Password"
        })
    )
    
    class Meta:
        model = User
        fields = ("new_password1", "new_password2")
        
    def clean_new_password1(self, *args, **kwargs):
        symbols = "@#_~[]{}()$&?%/"
        password = self.cleaned_data.get("new_password1")

        # MinimumLengthValidator
        if len(password) < 10:
            raise forms.ValidationError(
                "Password is too short. Requires a minimum of 10 characters")

        # CommonPasswordValidator
        if password.isdigit() or password.isalpha():
            raise forms.ValidationError("Password is too common.")

        # NoSymbolValidator
        if not any([sym in symbols for sym in password]):
            raise forms.ValidationError(
                f"Password should contain any of {symbols}")

        return password;

