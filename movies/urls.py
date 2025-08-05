"""
API URL configuration for the movies app.
"""
from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    # Local movie API endpoints
    path("api/movies/", views.MovieListAPIView.as_view(), name="movie_list_api"),
    path(
        "api/movies/<int:movie_id>/",
        views.MovieDetailAPIView.as_view(),
        name="movie_detail_api",
    ),
    path("api/genres/", views.GenreListAPIView.as_view(), name="genre_list_api"),
    # TMDb API endpoints
    path(
        "api/tmdb/popular/", views.PopularMoviesAPIView.as_view(), name="tmdb_popular"
    ),
    path(
        "api/tmdb/top-rated/",
        views.TopRatedMoviesAPIView.as_view(),
        name="tmdb_top_rated",
    ),
    path(
        "api/tmdb/now-playing/",
        views.NowPlayingMoviesAPIView.as_view(),
        name="tmdb_now_playing",
    ),
    path(
        "api/tmdb/upcoming/",
        views.UpcomingMoviesAPIView.as_view(),
        name="tmdb_upcoming",
    ),
    path("api/tmdb/search/", views.SearchMoviesAPIView.as_view(), name="tmdb_search"),
    path(
        "api/tmdb/movie/<int:tmdb_id>/",
        views.TMDbMovieDetailAPIView.as_view(),
        name="tmdb_movie_detail",
    ),
    path("api/tmdb/genres/", views.TMDbGenresAPIView.as_view(), name="tmdb_genres"),
    # Movie Recommendation API endpoints
    path(
        "api/recommendations/similar/<int:movie_id>/",
        views.SimilarMoviesAPIView.as_view(),
        name="similar_movies",
    ),
    path(
        "api/recommendations/based-on/<int:movie_id>/",
        views.MovieRecommendationsAPIView.as_view(),
        name="movie_recommendations",
    ),
    path(
        "api/recommendations/trending/",
        views.TrendingMoviesAPIView.as_view(),
        name="trending_movies",
    ),
    path(
        "api/recommendations/by-genre/",
        views.MoviesByGenreAPIView.as_view(),
        name="movies_by_genre",
    ),
    path(
        "api/recommendations/discover/",
        views.DiscoverMoviesAPIView.as_view(),
        name="discover_movies",
    ),
    # Health check
    path("api/health/", views.HealthCheckAPIView.as_view(), name="health_check"),
]
