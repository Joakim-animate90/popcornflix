# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-08-05

### Added
- **TMDb API Integration**: Complete integration with The Movie Database (TMDb) API
  - Bearer token authentication for TMDb API
  - Popular movies endpoint (`/api/tmdb/popular/`)
  - Top rated movies endpoint (`/api/tmdb/top-rated/`)
  - Now playing movies endpoint (`/api/tmdb/now-playing/`)
  - Upcoming movies endpoint (`/api/tmdb/upcoming/`)
  - Movie search endpoint (`/api/tmdb/search/`)
  - Movie details endpoint (`/api/tmdb/movie/{id}/`)
  - Genres endpoint (`/api/tmdb/genres/`)

- **API Documentation**: Comprehensive Swagger/OpenAPI documentation
  - Swagger UI available at `/api/docs/`
  - ReDoc documentation available at `/api/redoc/`
  - OpenAPI schema available at `/api/schema/`

- **Movie Management System**:
  - Movie model with TMDb integration fields
  - Genre model and many-to-many relationships
  - Database models for storing movie data locally

- **Management Commands**:
  - `sync_genres`: Synchronize genres from TMDb API
  - `sync_popular_movies`: Import popular movies from TMDb
  - `test_tmdb_api`: Test TMDb API connectivity

- **REST API Features**:
  - Class-based API views with proper error handling
  - Pagination support for all list endpoints
  - CORS headers for React frontend integration
  - Health check endpoint (`/api/health/`)

### Changed
- Converted from template-based views to pure REST API
- Updated authentication from API key to Bearer token for TMDb
- Enhanced error handling and response standardization

### Technical Details
- Django REST Framework integration
- PostgreSQL database support
- Environment-based configuration
- Type hints and comprehensive documentation
- Pre-commit hooks for code quality

## [1.0.0] - 2025-08-05

### Added
- Initial Django project setup
- PostgreSQL database configuration
- Basic project structure
- Git Flow workflow setup
- Pre-commit hooks (Black, isort, flake8)
- Environment configuration with python-dotenv
