"""
Request/response logging middleware for Day 78.
Logs all requests with method, path, status code, and response time.
"""

import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses.
    Tracks method, path, status code, duration, and errors.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Start timer
        start_time = time.time()
        
        # Extract request info
        method = request.method
        path = request.url.path
        query_string = request.url.query
        client_host = request.client.host if request.client else "unknown"
        
        # Log request
        logger.info(
            "Request received",
            extra={
                "method": method,
                "path": path,
                "query": query_string,
                "client": client_host,
            }
        )
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as exc:
            duration = time.time() - start_time
            logger.error(
                "Request failed",
                extra={
                    "method": method,
                    "path": path,
                    "duration_ms": round(duration * 1000, 2),
                    "error": str(exc),
                    "error_type": exc.__class__.__name__,
                },
                exc_info=True
            )
            raise
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            "Response sent",
            extra={
                "method": method,
                "path": path,
                "status": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
        )
        
        # Add response headers
        response.headers["X-Process-Time"] = str(duration)
        
        return response
