"""
TMDb API service for fetching movie data.
"""
import os
import requests
import logging
from typing import Dict, List, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class TMDbService:
    """Service class for interacting with The Movie Database API."""
    
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.bearer_token = os.getenv('TMDB_BEARER_TOKEN')
        self.base_url = os.getenv('TMDB_BASE_URL', 'https://api.themoviedb.org/3')
        
        if not self.bearer_token and not self.api_key:
            raise ValueError("Either TMDB_BEARER_TOKEN or TMDB_API_KEY environment variable is required")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for TMDb API requests."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        # Prefer Bearer token over API key
        if self.bearer_token:
            headers['Authorization'] = f'Bearer {self.bearer_token}'
        
        return headers
    
    def test_connection(self) -> bool:
        """Test the TMDb API connection."""
        try:
            # Test with a simple genres endpoint
            result = self.get_genres()
            return result is not None
        except Exception as e:
            logger.error(f"TMDb API connection test failed: {e}")
            return False
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to the TMDb API."""
        if params is None:
            params = {}
        
        # Only add API key to params if Bearer token is not available
        if not self.bearer_token and self.api_key:
            params['api_key'] = self.api_key
            
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error making request to TMDb API: {e} - Response: {response.text if 'response' in locals() else 'No response'}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error making request to TMDb API: {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON decode error from TMDb API: {e}")
            return None
    
    def get_popular_movies(self, page: int = 1) -> Optional[Dict]:
        """Get popular movies from TMDb."""
        #log request
        logger.info(f"Fetching popular movies from TMDb, page {page}")
        return self._make_request('movie/popular', {'page': page})
    
    def get_top_rated_movies(self, page: int = 1) -> Optional[Dict]:
        """Get top rated movies from TMDb."""
        return self._make_request('movie/top_rated', {'page': page})
    
    def get_now_playing_movies(self, page: int = 1) -> Optional[Dict]:
        """Get now playing movies from TMDb."""
        return self._make_request('movie/now_playing', {'page': page})
    
    def get_upcoming_movies(self, page: int = 1) -> Optional[Dict]:
        """Get upcoming movies from TMDb."""
        return self._make_request('movie/upcoming', {'page': page})
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed information about a specific movie."""
        return self._make_request(f'movie/{movie_id}')
    
    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """Search for movies by title."""
        return self._make_request('search/movie', {'query': query, 'page': page})
    
    def get_genres(self) -> Optional[Dict]:
        """Get list of movie genres."""
        return self._make_request('genre/movie/list')
    
    def get_movie_credits(self, movie_id: int) -> Optional[Dict]:
        """Get movie credits (cast and crew)."""
        return self._make_request(f'movie/{movie_id}/credits')
    
    def get_movie_videos(self, movie_id: int) -> Optional[Dict]:
        """Get movie videos (trailers, etc.)."""
        return self._make_request(f'movie/{movie_id}/videos')
    
    def get_similar_movies(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """Get movies similar to the given movie."""
        return self._make_request(f'movie/{movie_id}/similar', {'page': page})
    
    def get_movie_recommendations(self, movie_id: int, page: int = 1) -> Optional[Dict]:
        """Get movie recommendations based on the given movie."""
        return self._make_request(f'movie/{movie_id}/recommendations', {'page': page})
