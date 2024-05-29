from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccountModel


# Register your models here.
@admin.register(AccountModel)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number',)}),
    )