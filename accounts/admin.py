from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'email', 'age', 'is_staff']
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'age',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),
    )
