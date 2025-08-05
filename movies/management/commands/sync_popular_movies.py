"""
Management command to sync popular movies from TMDb API.
"""
from datetime import datetime

from django.core.management.base import BaseCommand

from movies.models import Genre, Movie, MovieGenre
from movies.services import TMDbService


class Command(BaseCommand):
    """Sync popular movies from TMDb API."""

    help = "Sync popular movies from TMDb API"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--pages", type=int, default=5, help="Number of pages to fetch (default: 5)"
        )

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            tmdb_service = TMDbService()
            pages = options["pages"]

            self.stdout.write(f"Fetching {pages} pages of popular movies from TMDb...")

            created_count = 0
            updated_count = 0

            for page in range(1, pages + 1):
                self.stdout.write(f"Processing page {page}...")

                movies_data = tmdb_service.get_popular_movies(page=page)
                if not movies_data:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to fetch page {page}")
                    )
                    continue

                movies = movies_data.get("results", [])

                for movie_data in movies:
                    try:
                        # Parse release date
                        release_date = None
                        if movie_data.get("release_date"):
                            try:
                                release_date = datetime.strptime(
                                    movie_data["release_date"], "%Y-%m-%d"
                                ).date()
                            except ValueError:
                                pass

                        # Create or update movie
                        movie, created = Movie.objects.update_or_create(
                            tmdb_id=movie_data["id"],
                            defaults={
                                "title": movie_data.get("title", ""),
                                "original_title": movie_data.get("original_title", ""),
                                "overview": movie_data.get("overview", ""),
                                "release_date": release_date,
                                "vote_average": movie_data.get("vote_average"),
                                "vote_count": movie_data.get("vote_count", 0),
                                "popularity": movie_data.get("popularity"),
                                "poster_path": movie_data.get("poster_path", ""),
                                "backdrop_path": movie_data.get("backdrop_path", ""),
                                "adult": movie_data.get("adult", False),
                                "video": movie_data.get("video", False),
                                "original_language": movie_data.get(
                                    "original_language", ""
                                ),
                            },
                        )

                        # Handle genres
                        if movie_data.get("genre_ids"):
                            # Clear existing genres for this movie
                            MovieGenre.objects.filter(movie=movie).delete()

                            # Add new genres
                            for genre_id in movie_data["genre_ids"]:
                                try:
                                    genre = Genre.objects.get(tmdb_id=genre_id)
                                    MovieGenre.objects.create(movie=movie, genre=genre)
                                except Genre.DoesNotExist:
                                    self.stdout.write(
                                        self.style.WARNING(
                                            f"Genre with TMDb ID {genre_id} not found. "
                                            "Run sync_genres command first."
                                        )
                                    )

                        if created:
                            created_count += 1
                            self.stdout.write(f"Created movie: {movie.title}")
                        else:
                            updated_count += 1
                            self.stdout.write(f"Updated movie: {movie.title}")

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error processing movie "
                                f'{movie_data.get("title", "Unknown")}: {str(e)}'
                            )
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully synced movies: {created_count} created, "
                    f"{updated_count} updated"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error syncing movies: {str(e)}"))
