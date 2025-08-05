"""
Serializers for the movies app API.
"""
from typing import Any, Dict, List, Optional

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Genre, Movie, MovieGenre


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model."""

    class Meta:
        model = Genre
        fields = ["id", "tmdb_id", "name"]


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model."""

    genres = serializers.SerializerMethodField()
    poster_url = serializers.ReadOnlyField()
    backdrop_url = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "tmdb_id",
            "title",
            "original_title",
            "overview",
            "release_date",
            "runtime",
            "vote_average",
            "vote_count",
            "popularity",
            "poster_path",
            "backdrop_path",
            "poster_url",
            "backdrop_url",
            "adult",
            "video",
            "original_language",
            "genres",
            "created_at",
            "updated_at",
        ]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_genres(self, obj: Movie) -> List[Dict[str, Any]]:
        """Get genres for the movie."""
        movie_genres = MovieGenre.objects.filter(movie=obj).select_related("genre")
        return [{"id": mg.genre.id, "name": mg.genre.name} for mg in movie_genres]


class TMDbMovieSerializer(serializers.Serializer):
    """Serializer for TMDb API movie data."""

    id = serializers.IntegerField()
    title = serializers.CharField()
    original_title = serializers.CharField(required=False, allow_blank=True)
    overview = serializers.CharField(required=False, allow_blank=True)
    release_date = serializers.DateField(required=False, allow_null=True)
    vote_average = serializers.FloatField(required=False, allow_null=True)
    vote_count = serializers.IntegerField(required=False, default=0)
    popularity = serializers.FloatField(required=False, allow_null=True)
    poster_path = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    backdrop_path = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    adult = serializers.BooleanField(required=False, default=False)
    video = serializers.BooleanField(required=False, default=False)
    original_language = serializers.CharField(required=False, allow_blank=True)
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )

    # Computed fields
    poster_url = serializers.SerializerMethodField()
    backdrop_url = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_poster_url(self, obj: Dict[str, Any]) -> Optional[str]:
        """Get full poster URL."""
        poster_path = obj.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_backdrop_url(self, obj: Dict[str, Any]) -> Optional[str]:
        """Get full backdrop URL."""
        backdrop_path = obj.get("backdrop_path")
        if backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280{backdrop_path}"
        return None


class TMDbMovieDetailSerializer(TMDbMovieSerializer):
    """Serializer for detailed TMDb movie data."""

    runtime = serializers.IntegerField(required=False, allow_null=True)
    budget = serializers.IntegerField(required=False, allow_null=True)
    revenue = serializers.IntegerField(required=False, allow_null=True)
    tagline = serializers.CharField(required=False, allow_blank=True)
    homepage = serializers.URLField(required=False, allow_blank=True)
    imdb_id = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    genres = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    production_companies = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    production_countries = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    spoken_languages = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
