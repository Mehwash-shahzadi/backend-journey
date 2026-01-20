# Day 76: Docker Compose Multi-Container Stack

## Overview

Complete multi-container application with FastAPI, PostgreSQL, and Redis running together via Docker Compose.

## What's Inside

**Three Services:**

1. **FastAPI App** - Main application on port 8000
2. **PostgreSQL** - Database with persistent volume
3. **Redis** - In-memory cache on port 6379

## Quick Start

```bash
# Start all services
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# View specific service logs
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f redis
```

## API Endpoints

### Health Checks

```bash
# Full health check
curl http://localhost:8000/health

# Database only
curl http://localhost:8000/health/db

# Redis only
curl http://localhost:8000/health/redis
```

### Cache Operations

```bash
# Set cache value
curl -X POST "http://localhost:8000/cache/set?key=mykey&value=myvalue"

# Get cache value
curl "http://localhost:8000/cache/get?key=mykey"
```

## Key Features

**Multi-Container Orchestration** - One command to run everything  
 **Environment Variables** - Configuration via .env  
 **Persistent Storage** - PostgreSQL data survives container restarts  
 **Health Checks** - Automatic service monitoring  
 **Networking** - Services communicate seamlessly  
 **Volume Management** - Data persistence across restarts

## Files Explanation

- **docker-compose.yml** - Orchestration configuration
- **Dockerfile** - App container build instructions
- **.env.example** - Environment variables template
- **main.py** - FastAPI application with service integration
- **requirements.txt** - Python dependencies

## Database Connection

Inside the container, PostgreSQL is accessible at:

```
postgresql://user:pass@db:5432/mydb
```

The service name `db` resolves automatically in the container network.

## Redis Connection

Inside the container, Redis is accessible at:

```
redis://redis:6379
```

The service name `redis` resolves automatically in the container network.

## Common Commands

```bash
# Execute command in running container
docker-compose exec app python -c "import requests; print(requests.get('http://localhost:8000/health').json())"

# View resource usage
docker-compose stats

# Remove all data (including volumes)
docker-compose down -v

# Rebuild images
docker-compose build

# Run specific service
docker-compose up db redis
```

## Testing Full Stack

```bash
# Check if all services are healthy
docker-compose ps

# Test database connection
curl http://localhost:8000/health/db

# Test Redis connection
curl http://localhost:8000/health/redis

# Store and retrieve cache
curl -X POST "http://localhost:8000/cache/set?key=test&value=hello"
curl "http://localhost:8000/cache/get?key=test"
```

## Troubleshooting

**Services failing to start:**

```bash
docker-compose logs app
docker-compose logs db
docker-compose logs redis
```

**Port already in use:**

```bash
# Change ports in docker-compose.yml or kill existing processes
lsof -i :8000
```

**Volume permission errors:**

```bash
# Fix volume permissions
docker-compose down -v
docker-compose up
```

## Key Learnings

- Docker Compose reduces "works on my machine" problems
- Services communicate via container names (DNS resolution)
- Volumes persist data even when containers stop
- Health checks ensure services are ready before use
- Environment variables enable configuration without code changes
- Networks isolate container communication

## Next Steps

- Add database migrations
- Implement connection pooling
- Set up log aggregation
- Add monitoring and metrics
- Deploy to production with proper secrets management
