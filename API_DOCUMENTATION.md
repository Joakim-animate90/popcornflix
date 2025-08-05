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

## Query Parameters

### Pagination
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

### Search
- `q` - Search query string (required for search endpoints)

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
