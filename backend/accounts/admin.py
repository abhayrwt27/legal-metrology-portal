from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Portal information", {
            "fields": ("role", "phone_number", "organization_name")
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Portal information", {
            "fields": ("role", "phone_number", "organization_name")
        }),
    )
