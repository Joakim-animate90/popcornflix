"""
URL patterns for user authentication and user-related operations.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "users"

urlpatterns = [
    # Authentication
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User Profile
    path("profile/", views.UserProfileView.as_view(), name="profile"),
    # Favorites
    path("favorites/", views.UserFavoriteListCreateView.as_view(), name="favorites"),
    path(
        "favorites/<int:pk>/",
        views.UserFavoriteDetailView.as_view(),
        name="favorite_detail",
    ),
    path(
        "favorites/check/<int:movie_id>/",
        views.check_favorite_status,
        name="check_favorite",
    ),
    # Watchlist
    path("watchlist/", views.UserWatchlistListCreateView.as_view(), name="watchlist"),
    path(
        "watchlist/<int:pk>/",
        views.UserWatchlistDetailView.as_view(),
        name="watchlist_detail",
    ),
    path(
        "watchlist/check/<int:movie_id>/",
        views.check_watchlist_status,
        name="check_watchlist",
    ),
]
