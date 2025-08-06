"""
URL configuration for popcornflix project - API only for React frontend.
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


@extend_schema(
    tags=["API Info"],
    summary="API Root",
    description=(
        "Root endpoint providing information about available API endpoints "
        "and documentation."
    ),
    responses={
        200: {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "version": {"type": "string"},
                "documentation": {
                    "type": "object",
                    "properties": {
                        "swagger_ui": {"type": "string"},
                        "redoc": {"type": "string"},
                        "openapi_schema": {"type": "string"},
                    },
                },
                "endpoints": {"type": "object"},
            },
        }
    },
)
@api_view(["GET"])
def api_root(request):
    """API root endpoint with available endpoints."""
    return Response(
        {
            "message": "Welcome to Popcornflix API",
            "version": "1.1.0",
            "documentation": {
                "swagger_ui": "/api/docs/",
                "redoc": "/api/redoc/",
                "openapi_schema": "/api/schema/",
            },
            "endpoints": {
                "health": "/api/health/",
                "authentication": {
                    "register": "/api/auth/register/",
                    "login": "/api/auth/login/",
                    "refresh": "/api/auth/token/refresh/",
                    "profile": "/api/auth/profile/",
                },
                "user_features": {
                    "favorites": "/api/auth/favorites/",
                    "watchlist": "/api/auth/watchlist/",
                    "check_favorite": "/api/auth/favorites/check/{movie_id}/",
                    "check_watchlist": "/api/auth/watchlist/check/{movie_id}/",
                },
                "movies": {
                    "local_movies": "/api/movies/",
                    "local_movie_detail": "/api/movies/{id}/",
                    "genres": "/api/genres/",
                },
                "tmdb": {
                    "popular": "/api/tmdb/popular/",
                    "top_rated": "/api/tmdb/top-rated/",
                    "now_playing": "/api/tmdb/now-playing/",
                    "upcoming": "/api/tmdb/upcoming/",
                    "search": "/api/tmdb/search/?q={query}",
                    "movie_detail": "/api/tmdb/movie/{tmdb_id}/",
                    "genres": "/api/tmdb/genres/",
                },
                "recommendations": {
                    "similar_movies": "/api/recommendations/similar/{movie_id}/",
                    "based_on_movie": "/api/recommendations/based-on/{movie_id}/",
                    "trending": "/api/recommendations/trending/",
                    "by_genre": "/api/recommendations/by-genre/?genres={genre_ids}",
                    "discover": "/api/recommendations/discover/",
                },
            },
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api_root"),
    path("", include("movies.urls")),
    path("api/auth/", include("users.urls")),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
