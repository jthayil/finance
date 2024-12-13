from django.forms import ModelForm, CharField, EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserModelForm(UserCreationForm, ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
