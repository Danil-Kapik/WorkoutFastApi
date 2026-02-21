# 🚀 Docker Quick Reference Card

## 📂 File Structure

```
FastAPIProject/
├── docker-compose.yml          ← Main orchestration
├── .dockerignore               ← Root context exclusion
├── .env.example                ← Config template
├── DOCKER_SETUP.md             ← Full documentation
├── DOCKER_IMPLEMENTATION.md    ← Implementation details
├── verify-docker-setup.sh      ← Verification script
│
├── app/
│   ├── Dockerfile              ← FastAPI backend image
│   ├── .dockerignore           ← Backend context exclusion
│   ├── main.py                 ← Updated CORS config
│   ├── core/
│   │   ├── config.py           ← Pydantic settings (reads .env)
│   │   └── database.py         ← Async SQLAlchemy setup
│   ├── alembic/
│   │   ├── env.py              ← Alembic config
│   │   └── versions/           ← Migration files
│   └── scripts/
│       └── initial_data.py     ← Database seeding
│
└── frontend/
    ├── Dockerfile              ← React + Nginx image
    ├── .dockerignore           ← Frontend context exclusion
    ├── nginx.conf              ← Nginx reverse proxy config
    └── package.json            ← Node dependencies
```

## ⚡ Essential Commands

### Initial Setup
```bash
# Copy environment template
cp .env.example .env

# Build and run everything
docker compose up --build
```

### Access Points
```
Frontend:     http://localhost
Backend API:  http://localhost:8000
API Docs:     http://localhost:8000/docs
Database:     localhost:5432
```

### Database Management
```bash
# Run migrations
docker compose exec backend alembic upgrade head

# Seed initial data
docker compose exec backend python -m app.scripts.initial_data

# Access database
docker compose exec db psql -U postgres -d fitness_db
```

### Container Management
```bash
# View logs
docker compose logs -f [service]

# Services: db, backend, frontend

# Stop everything
docker compose down

# Remove volumes (WARNING: deletes DB data)
docker compose down -v

# Restart service
docker compose restart backend
```

### Testing
```bash
# Run pytest
docker compose exec backend pytest

# Interactive bash
docker compose exec backend bash
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Client Browser                     │
└─────────────────┬───────────────────────────┘
                  │ http://localhost:80
        ┌─────────▼──────────────┐
        │   FRONTEND - NGINX      │
        │   ├─ / → SPA (React)    │
        │   └─ /api/* → Proxy     │
        └─────────┬──────────────┘
                  │ http://backend:8000
        ┌─────────▼──────────────┐
        │  BACKEND - FastAPI      │
        │  ├─ Uvicorn (8000)      │
        │  └─ Alembic migrations  │
        └─────────┬──────────────┘
                  │ postgresql://db:5432
        ┌─────────▼──────────────┐
        │   DATABASE - PostgreSQL │
        │   ├─ Async: asyncpg     │
        │   └─ Volume: postgres   │
        └────────────────────────┘
```

## 🔧 Environment Variables (.env)

```env
# Database
DB_HOST=db              # Docker service DNS
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=fitness_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 📊 Service Dependencies

```
db (PostgreSQL)
 ↑
 └─ (service_healthy condition)
 
 ↓
 
backend (FastAPI)
 ├─ Depends on: db (healthy)
 ├─ Runs: alembic migrate
 └─ Port: 8000
 
 ↓
 
frontend (Nginx)
 ├─ Depends on: backend (started)
 └─ Port: 80
```

## ✅ Health Checks

| Service  | Interval | Method | Retries |
|----------|----------|--------|---------|
| db       | 5s       | `pg_isready` | 5 |
| backend  | 30s      | `curl http://localhost:8000/` | 3 |
| frontend | 30s      | `wget http://localhost/` | 3 |

## 🚨 Common Issues & Fixes

### Backend won't start
```bash
docker compose logs backend
# Check: DB_HOST, DB_PORT in container
docker compose exec backend env | grep DB
```

### 502 Bad Gateway
```bash
docker compose ps
# Verify backend is healthy (HEALTHY in STATUS column)
docker compose exec frontend ping backend
```

### Database connection refused
```bash
docker compose logs db
# Wait for healthcheck to pass
docker compose ps
```

### Port already in use
```bash
# Change in docker-compose.yml:
# ports:
#   - "8001:8000"  # Use 8001 instead of 8000

docker compose restart backend
```

## 🔐 Security Notes

**Development (.env):**
```env
SECRET_KEY=dev-key-only-for-testing
```

**Production:**
```bash
export SECRET_KEY=$(openssl rand -hex 32)
docker run -e SECRET_KEY=$SECRET_KEY ...
```

## 📈 Performance Tuning

### Backend
```python
# Use uvloop for async performance (included)
uvicorn app.main:app --loop uvloop
```

### Frontend
```nginx
# Gzip compression (enabled in nginx.conf)
gzip on;
gzip_types text/css text/javascript ...;
```

### Database
```yaml
# Consider connection pooling in production
# PostgreSQL tuning parameters in env
```

## 🧪 Testing

```bash
# Unit tests
docker compose exec backend pytest

# With coverage
docker compose exec backend pytest --cov=app

# Specific test
docker compose exec backend pytest tests/test_auth.py -v
```

## 📦 Image Sizes

| Image | Size |
|-------|------|
| python:3.11-slim | ~160MB |
| node:18-alpine | ~180MB |
| nginx:stable-alpine | ~40MB |
| postgres:15-alpine | ~150MB |
| **Built images (compressed)** | **~200MB** |

## 🔄 Workflow

```
┌─────────────────────────────────────┐
│ 1. cp .env.example .env             │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ 2. docker compose up --build         │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ 3. Wait for healthchecks (20-30s)   │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ 4. Access http://localhost          │
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│ 5. Optional: Seed data, run tests   │
└─────────────────────────────────────┘
```

## 📚 Reference Files

- **DOCKER_SETUP.md** - Comprehensive guide
- **DOCKER_IMPLEMENTATION.md** - Implementation details
- **app/Dockerfile** - Backend build process
- **frontend/Dockerfile** - Frontend build process
- **frontend/nginx.conf** - Nginx configuration
- **docker-compose.yml** - Service orchestration

---

**Version:** 1.0 | **Status:** Production-Ready ✅
