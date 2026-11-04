from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Shelter, User


@admin.register(User)
class PawndMeUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('PawndMe', {'fields': ('account_type', 'shelter')}),
    )
    list_display = ('email', 'account_type', 'shelter', 'is_staff')


admin.site.register(Shelter)