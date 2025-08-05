"""
Admin configuration for movies app.
"""
from django.contrib import admin

from .models import Genre, Movie, MovieGenre


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin interface for Movie model."""

    list_display = ("title", "release_date", "vote_average", "popularity", "created_at")
    list_filter = ("release_date", "adult", "original_language", "created_at")
    search_fields = ("title", "original_title", "overview")
    readonly_fields = ("tmdb_id", "created_at", "updated_at")
    ordering = ("-popularity", "-vote_average")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("tmdb_id", "title", "original_title", "overview")},
        ),
        (
            "Release Information",
            {"fields": ("release_date", "runtime", "original_language")},
        ),
        (
            "Ratings & Popularity",
            {"fields": ("vote_average", "vote_count", "popularity")},
        ),
        ("Images", {"fields": ("poster_path", "backdrop_path")}),
        ("Flags", {"fields": ("adult", "video")}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin interface for Genre model."""

    list_display = ("name", "tmdb_id")
    search_fields = ("name",)
    readonly_fields = ("tmdb_id",)


@admin.register(MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    """Admin interface for MovieGenre model."""

    list_display = ("movie", "genre")
    list_filter = ("genre",)
    autocomplete_fields = ("movie",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("movie", "genre")
