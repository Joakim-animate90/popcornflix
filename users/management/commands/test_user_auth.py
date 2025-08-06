"""
Management command to test user authentication and favorites functionality.
"""
import json

import requests
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    """Test user authentication API endpoints."""

    help = "Test user authentication and favorites functionality"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--base-url",
            type=str,
            default="http://localhost:8000",
            help="Base URL for API testing (default: http://localhost:8000)",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        base_url = options["base_url"]

        self.stdout.write(self.style.SUCCESS("🎬 Testing User Authentication API..."))

        # Test data
        test_user = {
            "email": "test@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
        }

        try:
            # Test 1: User Registration
            self.stdout.write("\n1. Testing User Registration...")
            response = requests.post(
                f"{base_url}/api/auth/register/",
                json=test_user,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 201:
                self.stdout.write(self.style.SUCCESS("✅ User registration successful"))
                self.stdout.write(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Registration failed: {response.status_code}")
                )
                self.stdout.write(f"Error: {response.text}")
                return

            # Test 2: User Login
            self.stdout.write("\n2. Testing User Login...")
            login_data = {
                "email": test_user["email"],
                "password": test_user["password"],
            }

            response = requests.post(
                f"{base_url}/api/auth/login/",
                json=login_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("✅ User login successful"))
                tokens = response.json()
                access_token = tokens["access"]
                self.stdout.write(f"Access token received: {access_token[:50]}...")
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Login failed: {response.status_code}")
                )
                self.stdout.write(f"Error: {response.text}")
                return

            # Set authorization header for subsequent requests
            auth_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }

            # Test 3: Get User Profile
            self.stdout.write("\n3. Testing User Profile...")
            response = requests.get(
                f"{base_url}/api/auth/profile/", headers=auth_headers
            )

            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS("✅ Profile retrieval successful"))
                profile = response.json()
                self.stdout.write(f"Profile: {json.dumps(profile, indent=2)}")
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Profile retrieval failed: {response.status_code}"
                    )
                )

            # Test 4: Check if we have any movies to work with
            self.stdout.write("\n4. Checking available movies...")
            response = requests.get(f"{base_url}/api/movies/")

            if response.status_code == 200:
                movies = response.json()
                if movies.get("results"):
                    movie_id = movies["results"][0]["id"]
                    movie_title = movies["results"][0]["title"]
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Found movie to test with: {movie_title} "
                            f"(ID: {movie_id})"
                        )
                    )

                    # Test 5: Add to Favorites
                    self.stdout.write("\n5. Testing Add to Favorites...")
                    response = requests.post(
                        f"{base_url}/api/auth/favorites/",
                        json={"movie_id": movie_id},
                        headers=auth_headers,
                    )

                    if response.status_code == 201:
                        self.stdout.write(
                            self.style.SUCCESS("✅ Movie added to favorites")
                        )
                        favorite = response.json()
                        self.stdout.write(f"Favorite: {json.dumps(favorite, indent=2)}")
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ Add to favorites failed: {response.status_code}"
                            )
                        )
                        self.stdout.write(f"Error: {response.text}")

                    # Test 6: Check Favorite Status
                    self.stdout.write("\n6. Testing Check Favorite Status...")
                    response = requests.get(
                        f"{base_url}/api/auth/favorites/check/{movie_id}/",
                        headers=auth_headers,
                    )

                    if response.status_code == 200:
                        status_data = response.json()
                        if status_data.get("is_favorite"):
                            self.stdout.write(
                                self.style.SUCCESS(
                                    "✅ Movie is correctly marked as favorite"
                                )
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    "⚠️ Movie should be marked as favorite"
                                )
                            )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ Check favorite status failed: "
                                f"{response.status_code}"
                            )
                        )

                    # Test 7: List Favorites
                    self.stdout.write("\n7. Testing List Favorites...")
                    response = requests.get(
                        f"{base_url}/api/auth/favorites/", headers=auth_headers
                    )

                    if response.status_code == 200:
                        favorites = response.json()
                        items_count = len(favorites.get("results", []))
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✅ Favorites list retrieved: {items_count} items"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ List favorites failed: {response.status_code}"
                            )
                        )

                    # Test 8: Add to Watchlist
                    self.stdout.write("\n8. Testing Add to Watchlist...")
                    response = requests.post(
                        f"{base_url}/api/auth/watchlist/",
                        json={"movie_id": movie_id},
                        headers=auth_headers,
                    )

                    if response.status_code == 201:
                        self.stdout.write(
                            self.style.SUCCESS("✅ Movie added to watchlist")
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ Add to watchlist failed: {response.status_code}"
                            )
                        )
                        self.stdout.write(f"Error: {response.text}")

                    # Test 9: List Watchlist
                    self.stdout.write("\n9. Testing List Watchlist...")
                    response = requests.get(
                        f"{base_url}/api/auth/watchlist/", headers=auth_headers
                    )

                    if response.status_code == 200:
                        watchlist = response.json()
                        items_count = len(watchlist.get("results", []))
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✅ Watchlist retrieved: {items_count} items"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ List watchlist failed: {response.status_code}"
                            )
                        )

                else:
                    self.stdout.write(
                        self.style.WARNING(
                            "⚠️ No movies found in database. "
                            "Run sync_popular_movies first."
                        )
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ Failed to fetch movies: {response.status_code}"
                    )
                )

            self.stdout.write(
                self.style.SUCCESS("\n🎉 User Authentication API testing completed!")
            )

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Network error occurred: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Unexpected error: {str(e)}"))
