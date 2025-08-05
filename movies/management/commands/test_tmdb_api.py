"""
Management command to test TMDb API connection.
"""
from django.core.management.base import BaseCommand

from movies.services import TMDbService


class Command(BaseCommand):
    """Test TMDb API connection and configuration."""

    help = "Test TMDb API connection and configuration"

    def handle(self, *args, **options):
        """Execute the command."""
        try:
            self.stdout.write("Testing TMDb API connection...")

            tmdb_service = TMDbService()

            # Test connection
            if tmdb_service.test_connection():
                self.stdout.write(
                    self.style.SUCCESS("✅ TMDb API connection successful!")
                )

                # Test a few endpoints
                self.stdout.write("Testing endpoints...")

                # Test popular movies
                popular = tmdb_service.get_popular_movies(page=1)
                if popular and popular.get("results"):
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Popular movies: Found {len(popular["results"])} movies'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            "⚠️  Popular movies endpoint returned no results"
                        )
                    )

                # Test genres
                genres = tmdb_service.get_genres()
                if genres and genres.get("genres"):
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Genres: Found {len(genres["genres"])} genres'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("⚠️  Genres endpoint returned no results")
                    )

                # Test search
                search_results = tmdb_service.search_movies("batman")
                if search_results and search_results.get("results"):
                    results_count = len(search_results["results"])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Search: Found {results_count} results for "batman"'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("⚠️  Search endpoint returned no results")
                    )

            else:
                self.stdout.write(self.style.ERROR("❌ TMDb API connection failed!"))
                self.stdout.write(
                    "Please check your TMDB_BEARER_TOKEN or TMDB_API_KEY in .env file"
                )

        except ValueError as e:
            self.stdout.write(self.style.ERROR(f"❌ Configuration error: {str(e)}"))
            self.stdout.write(
                "Make sure TMDB_BEARER_TOKEN or TMDB_API_KEY is set in your .env file"
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Unexpected error: {str(e)}"))
