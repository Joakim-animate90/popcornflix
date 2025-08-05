# Popcornflix API Documentation

## Overview
The Popcornflix API provides endpoints for movie data integration with TMDb (The Movie Database) API. This API is designed to work with a React frontend application.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required for API endpoints.

## Endpoints

### Health Check
- **GET** `/api/health/` - Health check endpoint

### Local Movies (Database)
- **GET** `/api/movies/` - List all local movies (paginated)
- **GET** `/api/movies/{id}/` - Get movie detail by local ID
- **GET** `/api/genres/` - List all genres

### TMDb Integration
- **GET** `/api/tmdb/popular/` - Get popular movies from TMDb
- **GET** `/api/tmdb/top-rated/` - Get top rated movies from TMDb
- **GET** `/api/tmdb/now-playing/` - Get now playing movies from TMDb
- **GET** `/api/tmdb/upcoming/` - Get upcoming movies from TMDb
- **GET** `/api/tmdb/search/?q={query}` - Search movies on TMDb
- **GET** `/api/tmdb/movie/{tmdb_id}/` - Get detailed movie info from TMDb
- **GET** `/api/tmdb/genres/` - Get movie genres from TMDb

### Movie Recommendations
- **GET** `/api/recommendations/similar/{movie_id}/` - Get movies similar to a specific movie
- **GET** `/api/recommendations/based-on/{movie_id}/` - Get personalized recommendations based on a movie
- **GET** `/api/recommendations/trending/` - Get trending movies (day/week)
- **GET** `/api/recommendations/by-genre/` - Get movies filtered by genres
- **GET** `/api/recommendations/discover/` - Advanced movie discovery with multiple filters

## Query Parameters

### Pagination
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

### Search
- `q` - Search query string (required for search endpoints)

### Recommendations
- `genres` - Comma-separated list of genre IDs (for by-genre endpoint)
- `time_window` - "day" or "week" (for trending endpoint)
- `sort_by` - Sort criteria: "popularity.desc", "vote_average.desc", "release_date.desc", "revenue.desc"
- `primary_release_year` - Filter by specific release year
- `vote_average_gte` - Minimum vote average (0-10)
- `vote_count_gte` - Minimum number of votes
- `with_genres` - Genre IDs for advanced discovery

## Response Format

### Success Response
```json
{
  "results": [...],
  "page": 1,
  "total_pages": 100,
  "total_results": 2000
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## Movie Object Structure

### Local Movie
```json
{
  "id": 1,
  "tmdb_id": 550,
  "title": "Fight Club",
  "original_title": "Fight Club",
  "overview": "A ticking-time-bomb...",
  "release_date": "1999-10-15",
  "runtime": 139,
  "vote_average": 8.4,
  "vote_count": 26280,
  "popularity": 61.416,
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "backdrop_path": "/52AfXWuXCHn3UjD17rBruA9f5qb.jpg",
  "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "backdrop_url": "https://image.tmdb.org/t/p/w1280/52AfXWuXCHn3UjD17rBruA9f5qb.jpg",
  "adult": false,
  "video": false,
  "original_language": "en",
  "genres": [
    {"id": 1, "name": "Drama"}
  ],
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### TMDb Movie
```json
{
  "id": 550,
  "title": "Fight Club",
  "original_title": "Fight Club",
  "overview": "A ticking-time-bomb...",
  "release_date": "1999-10-15",
  "vote_average": 8.4,
  "vote_count": 26280,
  "popularity": 61.416,
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "backdrop_path": "/52AfXWuXCHn3UjD17rBruA9f5qb.jpg",
  "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "backdrop_url": "https://image.tmdb.org/t/p/w1280/52AfXWuXCHn3UjD17rBruA9f5qb.jpg",
  "adult": false,
  "video": false,
  "original_language": "en",
  "genre_ids": [18, 53]
}
```

## CORS Configuration
The API is configured to accept requests from:
- `http://localhost:3000` (React development server)
- `http://127.0.0.1:3000`

## Error Codes
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (TMDb API issues)

## Setup Requirements
1. Set `TMDB_BEARER_TOKEN` environment variable (preferred) or `TMDB_API_KEY`
2. Install requirements: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Test TMDb API connection: `python manage.py test_tmdb_api`
5. Start server: `python manage.py runserver`

## TMDb API Authentication
The service supports both authentication methods:
- **Bearer Token** (recommended): Set `TMDB_BEARER_TOKEN` in your `.env` file
- **API Key** (legacy): Set `TMDB_API_KEY` in your `.env` file

Bearer token authentication is preferred for better security and newer API features.

## Recommendation API Examples

### Similar Movies
```bash
GET /api/recommendations/similar/550/?page=1
# Get movies similar to Fight Club (TMDb ID: 550)
```

### Personalized Recommendations
```bash
GET /api/recommendations/based-on/550/?page=1
# Get personalized recommendations based on Fight Club
```

### Trending Movies
```bash
GET /api/recommendations/trending/?time_window=day&page=1
GET /api/recommendations/trending/?time_window=week&page=1
# Get trending movies for today or this week
```

### Movies by Genre
```bash
GET /api/recommendations/by-genre/?genres=28,12&sort_by=popularity.desc&page=1
# Get Action (28) and Adventure (12) movies sorted by popularity
```

### Advanced Discovery
```bash
GET /api/recommendations/discover/?with_genres=18&primary_release_year=2023&vote_average_gte=7.0&sort_by=vote_average.desc
# Discover Drama movies from 2023 with rating >= 7.0, sorted by rating
```

## Genre IDs Reference
Common TMDb genre IDs for recommendations:
- **28** - Action
- **12** - Adventure
- **16** - Animation
- **35** - Comedy
- **80** - Crime
- **99** - Documentary
- **18** - Drama
- **10751** - Family
- **14** - Fantasy
- **36** - History
- **27** - Horror
- **10402** - Music
- **9648** - Mystery
- **10749** - Romance
- **878** - Science Fiction
- **10770** - TV Movie
- **53** - Thriller
- **10752** - War
- **37** - Western
