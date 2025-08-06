"""
User models for authentication and user-related functionality.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from movies.models import Movie


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class UserFavorite(models.Model):
    """Model to store user's favorite movies."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_favorite"
        unique_together = ("user", "movie")
        verbose_name = "User Favorite"
        verbose_name_plural = "User Favorites"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.movie.title}"


class UserWatchlist(models.Model):
    """Model to store user's watchlist."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_watchlist"
        unique_together = ("user", "movie")
        verbose_name = "User Watchlist"
        verbose_name_plural = "User Watchlists"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.movie.title}"
