from fastapi import FastAPI
from app.database import Base, engine

# Import routers directly - IMPORTANT: Use exact file names
from app.routers.users import router as users_router
from app.routers.posts import router as posts_router
from app.routers.comments import router as comments_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Blog API",
    description="A professional RESTful API for managing blog posts, users, and comments. Built with FastAPI and PostgreSQL.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Include routers - IMPORTANT: This must happen after app creation
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    response_description="Welcome message with API information"
)
def root():
    """
    Root endpoint of the Blog API.

    Returns a welcome message and links to the interactive API documentation.
    This endpoint can be used to verify that the API is running correctly.

    Returns:
        dict: JSON object containing welcome message and documentation links
    """
    return {
        "message": "Welcome to Blog API",
        "version": "1.0.0",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_spec": "/openapi.json"
        },
        "endpoints": {
            "users": "/users",
            "posts": "/posts",
            "comments": "/comments"
        }
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check endpoint",
    response_description="API health status"
)
def health_check():
    """
    Health check endpoint.

    Returns the current status of the API service.
    Used for monitoring and ensuring the application is running properly.

    Returns:
        dict: JSON object with status information
    """
    return {
        "status": "healthy",
        "service": "Blog API",
        "version": "1.0.0"
    }