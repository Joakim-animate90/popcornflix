#!/bin/bash
# PopcornFlix Simple Deployment Script
# Uses the latest tag which automatically points to the highest semantic version

set -e

# Configuration
REGISTRY="ghcr.io"
IMAGE_NAME="joakim-animate90/popcornflix-backend"
FULL_IMAGE="${REGISTRY}/${IMAGE_NAME}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

echo "🍿 PopcornFlix Deployment"
echo "========================"

# Parse command line arguments
VERSION="${1:-latest}"
PORT="${2:-8000}"
CONTAINER_NAME="popcornflix-app"

print_info "Deploying PopcornFlix with version: $VERSION on port: $PORT"

# Pull the image
print_info "Pulling latest image..."
docker pull "${FULL_IMAGE}:${VERSION}"

# Stop and remove existing container if running
if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
    print_info "Stopping existing container..."
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1
fi

# Run the container
print_info "Starting container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:8000" \
    -e DEBUG="${DEBUG:-False}" \
    -e SECRET_KEY="${SECRET_KEY:-$(openssl rand -base64 32)}" \
    -e DB_ENGINE="${DB_ENGINE:-django.db.backends.postgresql}" \
    -e DB_NAME="${DB_NAME:-popcornflix}" \
    -e DB_USER="${DB_USER:-postgres}" \
    -e DB_PASSWORD="${DB_PASSWORD:-postgres}" \
    -e DB_HOST="${DB_HOST:-localhost}" \
    -e DB_PORT="${DB_PORT:-5432}" \
    "${FULL_IMAGE}:${VERSION}"

print_success "PopcornFlix deployed successfully!"
print_info "Access your application at: http://localhost:$PORT"
print_info "Container name: $CONTAINER_NAME"

echo ""
echo "Usage: $0 [version] [port]"
echo "Examples:"
echo "  $0                    # Deploy latest version on port 8000"
echo "  $0 latest 8080        # Deploy latest version on port 8080"
echo "  $0 v1.2.3             # Deploy specific version v1.2.3"
