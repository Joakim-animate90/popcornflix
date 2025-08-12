# 🍿 PopcornFlix

<div align="center">

![Version](https://img.shields.io/badge/version-1.6.2-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

**A modern, feature-rich movie streaming platform API built with Django and integrated with The Movie Database (TMDb)**

[🚀 Live Demo](#) • [📖 Documentation](./API_DOCUMENTATION.md) • [🐳 Docker Setup](./DOCKER_DEPLOYMENT.md) • [🔐 Authentication](./USER_AUTH_FEATURE.md)

</div>

---

## ✨ Features

### 🎬 Movie Management
- **TMDb Integration** - Real-time movie data from The Movie Database
- **Local Database** - Efficient caching of movie information
- **Advanced Search** - Find movies by title, genre, year, rating
- **Smart Recommendations** - Similar movies and personalized suggestions
- **Rich Metadata** - Detailed movie information including posters, ratings, cast

### 🔐 User Authentication & Personalization
- **JWT Authentication** - Secure token-based authentication
- **Custom User Model** - Email-based authentication
- **Favorites System** - Save your favorite movies
- **Watchlist** - Keep track of movies to watch later
- **User Profiles** - Manage your personal information

### 🛠️ Developer Experience
- **REST API** - Comprehensive RESTful API endpoints
- **OpenAPI Documentation** - Interactive Swagger/ReDoc documentation
- **Docker Ready** - Containerized deployment
- **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- **Code Quality** - Pre-commit hooks, linting, and formatting

### 📊 Advanced Filtering & Discovery
- **Genre-based Filtering** - Discover movies by genre preferences
- **Multi-criteria Search** - Filter by year, rating, popularity
- **Trending Movies** - Stay updated with trending content
- **Now Playing & Upcoming** - Latest and upcoming movie releases

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL
- Docker (optional)

### 🐳 Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/Joakim-animate90/popcornflix.git
cd popcornflix

# Pull and run the latest Docker image
docker pull ghcr.io/joakim-animate90/popcornflix-backend:latest
docker-compose up -d
```

### 🔧 Local Development Setup

1. **Clone & Navigate**
   ```bash
   git clone https://github.com/Joakim-animate90/popcornflix.git
   cd popcornflix
   ```

2. **Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Setup Pre-commit Hooks** (Development)
   ```bash
   pre-commit install
   ```

---

## 📋 Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=popcornflix
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# TMDb API
TMDB_API_KEY=your_tmdb_api_key

# CORS Settings (for frontend integration)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend-domain.com
```

---

## 📡 API Endpoints

### 🔐 Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | User registration |
| `/api/auth/login/` | POST | User login (JWT tokens) |
| `/api/auth/token/refresh/` | POST | Refresh JWT token |
| `/api/auth/profile/` | GET/PUT | User profile management |

### 🎬 Movies
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/movies/` | GET | Local movie database |
| `/api/movies/{id}/` | GET | Movie details |
| `/api/genres/` | GET | Available genres |
| `/api/tmdb/popular/` | GET | Popular movies from TMDb |
| `/api/tmdb/search/` | GET | Search movies |

### ❤️ User Features
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/favorites/` | GET/POST | Manage favorites |
| `/api/auth/favorites/{movie_id}/` | DELETE | Remove from favorites |
| `/api/auth/watchlist/` | GET/POST | Manage watchlist |
| `/api/auth/favorites/check/{movie_id}/` | GET | Check favorite status |

### 🔍 Recommendations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/recommendations/similar/{movie_id}/` | GET | Similar movies |
| `/api/recommendations/trending/` | GET | Trending movies |
| `/api/recommendations/by-genre/` | GET | Movies by genre |
| `/api/recommendations/discover/` | GET | Advanced movie discovery |

---

## 📖 Documentation

- **[API Documentation](./API_DOCUMENTATION.md)** - Complete API reference
- **[Docker Deployment](./DOCKER_DEPLOYMENT.md)** - Container deployment guide
- **[User Authentication](./USER_AUTH_FEATURE.md)** - Authentication system details
- **[Interactive API Docs](http://localhost:8000/api/docs/)** - Swagger UI (when running)
- **[ReDoc Documentation](http://localhost:8000/api/redoc/)** - Alternative API docs

---

## 🛠️ Technology Stack

### Backend
- **Django 5.2.4** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Primary database
- **Redis** - Caching (optional)

### Authentication & Security
- **JWT (djangorestframework-simplejwt)** - Token authentication
- **CORS Headers** - Cross-origin resource sharing
- **WhiteNoise** - Static file serving

### External Services
- **TMDb API** - Movie data integration
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipeline

### Development Tools
- **Pre-commit** - Code quality hooks
- **Black** - Code formatting
- **isort** - Import sorting
- **Flake8** - Linting
- **drf-spectacular** - API documentation

---

## 🔄 Development Workflow

This project uses **Git Flow** branching strategy:

- `main` - Production-ready releases
- `develop` - Integration branch for features
- `feature/*` - Individual feature development

### Automated Workflows
- **Continuous Integration** - Automated testing on pull requests
- **Docker Builds** - Automatic image building and publishing
- **Security Scanning** - Vulnerability detection with Trivy
- **Auto-releases** - Semantic versioning and automated releases

---

## 🐳 Docker

### Quick Start
```bash
# Pull the latest image
docker pull ghcr.io/joakim-animate90/popcornflix-backend:latest

# Run with Docker Compose
docker-compose up -d
```

### Available Tags
- `latest` - Latest stable release
- `v1.6.2` - Specific version
- `develop` - Development version

---

## 📊 Project Structure

```
popcornflix/
├── movies/                 # Movie app (models, views, serializers)
├── users/                  # User authentication and profiles
├── popcornflix/            # Django project settings
├── .github/workflows/      # CI/CD pipelines
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
└── manage.py              # Django management script
```

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use conventional commit messages

---

## 🔒 Security

- JWT tokens for secure authentication
- Environment variable configuration
- CORS protection
- SQL injection prevention through Django ORM
- Regular security updates through automated workflows

---

## 📈 Performance

- **Database Optimization** - Efficient queries with select_related and prefetch_related
- **Caching** - TMDb API response caching
- **Pagination** - Efficient data loading
- **Static File Optimization** - WhiteNoise compression

---

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check your .env database configuration
# Ensure PostgreSQL is running
sudo systemctl start postgresql
```

**TMDb API Issues**
```bash
# Verify your TMDb API key in .env
# Check API rate limits
```

**Docker Issues**
```bash
# Rebuild containers
docker-compose down && docker-compose up --build
```

---

## 📝 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and release notes.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [The Movie Database (TMDb)](https://www.themoviedb.org/) for providing movie data
- [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/) communities
- All contributors and users of this project

---

<div align="center">

**[⬆ Back to Top](#-popcornflix)**

Made with ❤️ by [Joakim-animate90](https://github.com/Joakim-animate90)

</div>
