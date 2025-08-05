"""
Management command to test the movie recommendation API functionality.
"""
from django.core.management.base import BaseCommand

from movies.services import TMDbService


class Command(BaseCommand):
    help = "Test the movie recommendation API functionality"

    def add_arguments(self, parser):
        parser.add_argument(
            "--movie-id",
            type=int,
            default=550,  # Fight Club
            help="TMDb movie ID to test recommendations (default: 550 - Fight Club)",
        )

    def handle(self, *args, **options):
        movie_id = options["movie_id"]

        self.stdout.write(
            self.style.SUCCESS(
                f"Testing Movie Recommendation API with movie ID: {movie_id}"
            )
        )

        try:
            tmdb_service = TMDbService()

            # Test connection
            self.stdout.write("1. Testing TMDb API connection...")
            if tmdb_service.test_connection():
                self.stdout.write(
                    self.style.SUCCESS("   ✓ TMDb API connection successful")
                )
            else:
                self.stdout.write(self.style.ERROR("   ✗ TMDb API connection failed"))
                return

            # Test movie details
            self.stdout.write(f"\n2. Getting movie details for ID {movie_id}...")
            movie_details = tmdb_service.get_movie_details(movie_id)
            if movie_details:
                title = movie_details.get("title", "Unknown")
                year = (
                    movie_details.get("release_date", "Unknown")[:4]
                    if movie_details.get("release_date")
                    else "Unknown"
                )
                self.stdout.write(
                    self.style.SUCCESS(f'   ✓ Found movie: "{title}" ({year})')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"   ✗ Movie with ID {movie_id} not found")
                )
                return

            # Test similar movies
            self.stdout.write("\n3. Getting similar movies...")
            similar_movies = tmdb_service.get_similar_movies(movie_id)
            if similar_movies and similar_movies.get("results"):
                count = len(similar_movies["results"])
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Found {count} similar movies")
                )
                for i, movie in enumerate(similar_movies["results"][:3], 1):
                    title = movie.get("title", "Unknown")
                    vote_avg = movie.get("vote_average", 0)
                    self.stdout.write(f"      {i}. {title} (Rating: {vote_avg})")
            else:
                self.stdout.write(self.style.WARNING("   ! No similar movies found"))

            # Test movie recommendations
            self.stdout.write("\n4. Getting movie recommendations...")
            recommendations = tmdb_service.get_movie_recommendations(movie_id)
            if recommendations and recommendations.get("results"):
                count = len(recommendations["results"])
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Found {count} recommended movies")
                )
                for i, movie in enumerate(recommendations["results"][:3], 1):
                    title = movie.get("title", "Unknown")
                    vote_avg = movie.get("vote_average", 0)
                    self.stdout.write(f"      {i}. {title} (Rating: {vote_avg})")
            else:
                self.stdout.write(
                    self.style.WARNING("   ! No movie recommendations found")
                )

            # Test trending movies
            self.stdout.write("\n5. Getting trending movies...")
            trending = tmdb_service.get_trending_movies("day")
            if trending and trending.get("results"):
                count = len(trending["results"])
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Found {count} trending movies")
                )
                for i, movie in enumerate(trending["results"][:3], 1):
                    title = movie.get("title", "Unknown")
                    popularity = movie.get("popularity", 0)
                    self.stdout.write(
                        f"      {i}. {title} (Popularity: {popularity:.1f})"
                    )
            else:
                self.stdout.write(self.style.WARNING("   ! No trending movies found"))

            # Test movies by genre (Action = 28)
            self.stdout.write("\n6. Getting action movies by genre...")
            action_movies = tmdb_service.get_movies_by_genre([28])  # Action genre ID
            if action_movies and action_movies.get("results"):
                count = len(action_movies["results"])
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Found {count} action movies")
                )
                for i, movie in enumerate(action_movies["results"][:3], 1):
                    title = movie.get("title", "Unknown")
                    vote_avg = movie.get("vote_average", 0)
                    self.stdout.write(f"      {i}. {title} (Rating: {vote_avg})")
            else:
                self.stdout.write(self.style.WARNING("   ! No action movies found"))

            # Test discover movies
            self.stdout.write("\n7. Testing movie discovery...")
            discover_movies = tmdb_service.discover_movies(
                vote_average_gte=7.0, vote_count_gte=1000, sort_by="vote_average.desc"
            )
            if discover_movies and discover_movies.get("results"):
                count = len(discover_movies["results"])
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ Discovered {count} high-rated movies")
                )
                for i, movie in enumerate(discover_movies["results"][:3], 1):
                    title = movie.get("title", "Unknown")
                    vote_avg = movie.get("vote_average", 0)
                    vote_count = movie.get("vote_count", 0)
                    self.stdout.write(
                        f"      {i}. {title} (Rating: {vote_avg}, Votes: {vote_count})"
                    )
            else:
                self.stdout.write(self.style.WARNING("   ! No movies discovered"))

            self.stdout.write(
                self.style.SUCCESS(
                    "\n🎬 Movie recommendation API test completed successfully!"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error testing recommendation API: {str(e)}")
            )
