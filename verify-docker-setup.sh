#!/bin/bash
# Docker Setup Verification Script

set -e

echo "🔍 Docker Setup Verification"
echo "=============================="
echo ""

# Check Docker installation
echo "✓ Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi
echo "  Docker version: $(docker --version)"

# Check Docker Compose installation
echo "✓ Checking Docker Compose installation..."
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi
echo "  Docker Compose version: $(docker compose version)"

echo ""
echo "✓ Checking Docker files..."

# Check required files
required_files=(
    "docker-compose.yml"
    "app/Dockerfile"
    "app/.dockerignore"
    "frontend/Dockerfile"
    "frontend/.dockerignore"
    "frontend/nginx.conf"
    ".env.example"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ❌ $file missing"
        exit 1
    fi
done

echo ""
echo "✓ Checking .env file..."
if [ ! -f ".env" ]; then
    echo "  ⚠️  .env file not found, creating from .env.example..."
    cp .env.example .env
    echo "  ✓ .env created (using default values)"
else
    echo "  ✓ .env file exists"
fi

echo ""
echo "📦 Docker Image Build Information"
echo "=================================="
echo ""
echo "Backend Dockerfile:"
echo "  Base image: python:3.11-slim"
echo "  Build args: None (uses requirements.txt)"
echo "  Exposed port: 8000"
echo ""
echo "Frontend Dockerfile:"
echo "  Build stage: node:18-alpine"
echo "  Production stage: nginx:stable-alpine"
echo "  Exposed port: 80"
echo ""
echo "Database:"
echo "  Image: postgres:15-alpine"
echo "  Exposed port: 5432"
echo ""

echo "🚀 Ready to start!"
echo "=================================="
echo ""
echo "Run the following command to start the project:"
echo ""
echo "  docker compose up --build"
echo ""
echo "After services are healthy, access:"
echo "  • Frontend: http://localhost"
echo "  • Backend API: http://localhost:8000"
echo "  • API Docs: http://localhost:8000/docs"
echo "  • Database: localhost:5432"
echo ""
