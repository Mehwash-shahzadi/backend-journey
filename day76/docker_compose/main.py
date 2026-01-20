import os
from fastapi import FastAPI
import psycopg2
import redis
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Multi-Container Stack")

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/mydb")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


@app.get("/")
def read_root():
    return {"message": "Multi-container stack running", "components": ["FastAPI", "PostgreSQL", "Redis"]}


@app.get("/health/db")
def check_database():
    """Check PostgreSQL connection."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return {"status": "healthy", "database": "PostgreSQL connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/health/redis")
def check_redis():
    """Check Redis connection."""
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
        return {"status": "healthy", "cache": "Redis connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.get("/health")
def full_health_check():
    """Check all components."""
    db_status = "healthy"
    redis_status = "healthy"
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
    except:
        db_status = "unhealthy"
    
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
    except:
        redis_status = "unhealthy"
    
    overall = "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded"
    
    return {
        "status": overall,
        "database": db_status,
        "cache": redis_status
    }


@app.post("/cache/set")
def set_cache(key: str, value: str):
    """Store a value in Redis cache."""
    try:
        r = redis.from_url(REDIS_URL)
        r.set(key, value, ex=3600)  # Expires in 1 hour
        return {"status": "success", "key": key, "value": value}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/cache/get")
def get_cache(key: str):
    """Retrieve a value from Redis cache."""
    try:
        r = redis.from_url(REDIS_URL)
        value = r.get(key)
        if value:
            return {"status": "found", "key": key, "value": value.decode()}
        return {"status": "not_found", "key": key}
    except Exception as e:
        return {"status": "error", "error": str(e)}
