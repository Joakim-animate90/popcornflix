# User Authentication and Favorites Feature

## Summary
Added comprehensive user authentication system with JWT tokens and user favorites/watchlist functionality.

## New Features

### Authentication
- Custom User model extending AbstractUser
- JWT token authentication using djangorestframework-simplejwt
- User registration and login endpoints
- User profile management

### User Features
- Add/remove movies from favorites
- Add/remove movies from watchlist
- Check favorite/watchlist status for movies
- List user's favorites and watchlist

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile

### User Favorites
- `GET /api/auth/favorites/` - List user favorites
- `POST /api/auth/favorites/` - Add movie to favorites
- `DELETE /api/auth/favorites/{id}/` - Remove from favorites
- `GET /api/auth/favorites/check/{movie_id}/` - Check favorite status

### User Watchlist
- `GET /api/auth/watchlist/` - List user watchlist
- `POST /api/auth/watchlist/` - Add movie to watchlist
- `DELETE /api/auth/watchlist/{id}/` - Remove from watchlist
- `GET /api/auth/watchlist/check/{movie_id}/` - Check watchlist status

## Models
- `User` - Custom user model with email as username
- `UserFavorite` - User's favorite movies
- `UserWatchlist` - User's watchlist movies

## Configuration
- JWT settings configured with 60-minute access tokens and 7-day refresh tokens
- Custom authentication classes in REST_FRAMEWORK settings
- Database recreated to support custom user model

## Testing
- Management command `test_user_auth` to verify all authentication functionality

## Note
Movie browsing endpoints remain publicly accessible, while user-specific features require authentication.
