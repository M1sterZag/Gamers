from django.contrib import admin
from .models import AuthUser


@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_premium", "created_at")
    list_display_links = ("email",)
    readonly_fields = ("created_at",)