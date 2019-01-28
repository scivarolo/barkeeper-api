from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import BarkeeperUserCreationForm, BarkeeperUserChangeForm
from .models import BarkeeperUser
# Register your models here.

class BarkeeperUserAdmin(UserAdmin):
    add_form = BarkeeperUserCreationForm
    form = BarkeeperUserChangeForm
    model = BarkeeperUser
    list_display = ['email', 'username',]

admin.site.register(BarkeeperUser, BarkeeperUserAdmin)