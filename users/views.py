"""
Views for user authentication and user-related operations.
"""
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from movies.models import Movie

from .models import UserFavorite, UserWatchlist
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserFavoriteSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserWatchlistSerializer,
)

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="User registration",
        description="Register a new user account with email and password.",
    )
)
class UserRegistrationView(generics.CreateAPIView):
    """View for user registration."""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="User login",
        description="Login with email and password to get JWT tokens.",
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view."""

    serializer_class = CustomTokenObtainPairSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["User Profile"],
        summary="Get user profile",
        description="Get the current user's profile information.",
    ),
    put=extend_schema(
        tags=["User Profile"],
        summary="Update user profile",
        description="Update the current user's profile information.",
    ),
    patch=extend_schema(
        tags=["User Profile"],
        summary="Partial update user profile",
        description="Partially update the current user's profile information.",
    ),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for user profile management."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    get=extend_schema(
        tags=["User Favorites"],
        summary="List user favorites",
        description="Get the current user's favorite movies.",
    ),
    post=extend_schema(
        tags=["User Favorites"],
        summary="Add movie to favorites",
        description="Add a movie to the current user's favorites.",
    ),
)
class UserFavoriteListCreateView(generics.ListCreateAPIView):
    """View for listing and creating user favorites."""

    serializer_class = UserFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        movie_id = serializer.validated_data["movie_id"]
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie_id": "Movie not found."})

        # Check if already in favorites
        if UserFavorite.objects.filter(user=self.request.user, movie=movie).exists():
            raise serializers.ValidationError(
                {"detail": "Movie is already in favorites."}
            )

        serializer.save(user=self.request.user, movie=movie)


@extend_schema_view(
    delete=extend_schema(
        tags=["User Favorites"],
        summary="Remove movie from favorites",
        description="Remove a movie from the current user's favorites.",
    )
)
class UserFavoriteDetailView(generics.DestroyAPIView):
    """View for removing favorites."""

    serializer_class = UserFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        tags=["User Watchlist"],
        summary="List user watchlist",
        description="Get the current user's watchlist movies.",
    ),
    post=extend_schema(
        tags=["User Watchlist"],
        summary="Add movie to watchlist",
        description="Add a movie to the current user's watchlist.",
    ),
)
class UserWatchlistListCreateView(generics.ListCreateAPIView):
    """View for listing and creating user watchlist items."""

    serializer_class = UserWatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        movie_id = serializer.validated_data["movie_id"]
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise serializers.ValidationError({"movie_id": "Movie not found."})

        # Check if already in watchlist
        if UserWatchlist.objects.filter(user=self.request.user, movie=movie).exists():
            raise serializers.ValidationError(
                {"detail": "Movie is already in watchlist."}
            )

        serializer.save(user=self.request.user, movie=movie)


@extend_schema_view(
    delete=extend_schema(
        tags=["User Watchlist"],
        summary="Remove movie from watchlist",
        description="Remove a movie from the current user's watchlist.",
    )
)
class UserWatchlistDetailView(generics.DestroyAPIView):
    """View for removing watchlist items."""

    serializer_class = UserWatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserWatchlist.objects.filter(user=self.request.user)


@extend_schema(
    tags=["User Favorites"],
    summary="Check if movie is favorited",
    description="Check if a specific movie is in the user's favorites.",
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def check_favorite_status(request, movie_id):
    """Check if a movie is in user's favorites."""
    try:
        movie = Movie.objects.get(id=movie_id)
        is_favorite = UserFavorite.objects.filter(
            user=request.user, movie=movie
        ).exists()
        return Response({"is_favorite": is_favorite})
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=["User Watchlist"],
    summary="Check if movie is in watchlist",
    description="Check if a specific movie is in the user's watchlist.",
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def check_watchlist_status(request, movie_id):
    """Check if a movie is in user's watchlist."""
    try:
        movie = Movie.objects.get(id=movie_id)
        is_in_watchlist = UserWatchlist.objects.filter(
            user=request.user, movie=movie
        ).exists()
        return Response({"is_in_watchlist": is_in_watchlist})
    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
