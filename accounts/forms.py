from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BarkeeperUser

class BarkeeperUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = BarkeeperUser
        fields = ('username', 'email')


class BarkeeperUserChangeForm(UserChangeForm):

    class Meta:
        model = BarkeeperUser
        fields = ('username', 'email')