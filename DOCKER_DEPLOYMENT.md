# 🐳 Docker Deployment Guide

## GitHub Container Registry

This project automatically builds and pushes Docker images to GitHub Container Registry (GHCR) with proper versioning.

### Image Tags

- `ghcr.io/joakim-animate90/popcornflix-backend:latest` - Latest build from main branch
- `ghcr.io/joakim-animate90/popcornflix-backend:1.0.0` - Specific version
- `ghcr.io/joakim-animate90/popcornflix-backend:1.0` - Major.minor version
- `ghcr.io/joakim-animate90/popcornflix-backend:1` - Major version

### Automated Builds

**On Push to Main/Develop:**
- Builds and pushes development images
- Tags with branch name and commit SHA

**On Git Tag (v*.*.*):**
- Builds production-ready images
- Creates semantic version tags
- Generates GitHub release
- Runs security scans

### Creating a Release

1. **Using Git Tags:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. **Using GitHub Actions (Manual):**
- Go to Actions tab
- Run "Release and Deploy" workflow
- Enter version number (e.g., 1.0.0)

### Deployment

#### Pull and Run
```bash
# Pull specific version
docker pull ghcr.io/joakim-animate90/popcornflix-backend:1.0.0

# Run with environment variables
docker run -d \
  --name popcornflix-backend \
  -p 8000:8000 \
  -e DB_HOST=your-db-host \
  -e DB_NAME=popcornflix \
  -e DB_USER=your-user \
  -e DB_PASSWORD=your-password \
  -e TMDB_BEARER_TOKEN=your-token \
  ghcr.io/joakim-animate90/popcornflix-backend:1.0.0
```

#### Using Docker Compose
```yaml
version: '3.8'
services:
  web:
    image: ghcr.io/joakim-animate90/popcornflix-backend:1.0.0
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - DB_NAME=popcornflix
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - TMDB_BEARER_TOKEN=${TMDB_BEARER_TOKEN}
```

### Environment Variables

Required:
- `DB_HOST` - Database host
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `TMDB_BEARER_TOKEN` - TMDb API bearer token

Optional:
- `DEBUG` - Enable debug mode (default: False)
- `SECRET_KEY` - Django secret key (auto-generated if not set)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

### Health Check

The image includes a health check endpoint:
```bash
curl http://localhost:8000/api/
```

### Security

- Images are scanned with Trivy for vulnerabilities
- Multi-arch support (AMD64, ARM64)
- Non-root user execution
- Minimal attack surface with Alpine-based images
