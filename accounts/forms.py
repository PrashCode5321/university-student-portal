from typing import Any, Dict
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    """def clean(self):
        if self.errors:
            self.fields["username"].widget.attrs["class"] = "form-control is-invalid"
            self.fields["password"].widget.attrs["class"] = "form-control is-invalid"
        super().clean()"""
