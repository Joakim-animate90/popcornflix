"""
Admin configuration for user authentication and user-related models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserFavorite, UserWatchlist


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    """Admin configuration for UserFavorite model."""

    list_display = ("user", "movie", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "user__username", "movie__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(UserWatchlist)
class UserWatchlistAdmin(admin.ModelAdmin):
    """Admin configuration for UserWatchlist model."""

    list_display = ("user", "movie", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "user__username", "movie__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
