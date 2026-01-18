import logging
import json
import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import httpx

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for comprehensive error handling.
    Catches exceptions and returns user-friendly responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Intercept request/response to handle errors.
        
        Day 74 Feature: Enhanced error tracking with request context
        """
        request_id = str(time.time())  # Simple request ID
        start_time = time.time()
        
        try:
            response = await call_next(request)
            
            # Log successful requests (info level)
            duration = time.time() - start_time
            if response.status_code >= 400:
                logger.warning(
                    f"[{request_id}] {request.method} {request.url.path} "
                    f"- Status {response.status_code} ({duration:.2f}s)"
                )
            else:
                logger.info(
                    f"[{request_id}] {request.method} {request.url.path} "
                    f"- Status {response.status_code} ({duration:.2f}s)"
                )
            
            return response
        
        except httpx.TimeoutException as e:
            # LLM timeout error (Day 74)
            logger.error(
                f"[{request_id}] TIMEOUT: LLM request exceeded timeout limit. "
                f"Endpoint: {request.url.path}, Details: {str(e)}"
            )
            return JSONResponse(
                status_code=504,
                content={
                    "detail": "The AI service took too long to respond. Please try again in a moment.",
                    "error_code": "LLM_TIMEOUT",
                    "request_id": request_id
                }
            )
        
        except httpx.HTTPStatusError as e:
            # LLM API errors (429, 500, etc.) - Day 74
            if e.response.status_code == 429:
                logger.error(
                    f"[{request_id}] RATE_LIMITED: Gemini API rate limit exceeded. "
                    f"Will retry after cool-down period."
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "The AI service is currently busy. Please try again in 1-2 minutes.",
                        "error_code": "LLM_RATE_LIMIT",
                        "request_id": request_id
                    }
                )
            elif e.response.status_code == 500:
                logger.error(
                    f"[{request_id}] LLM_ERROR: Gemini API returned 500. "
                    f"Details: {str(e)}"
                )
                return JSONResponse(
                    status_code=503,
                    content={
                        "detail": "The AI service is temporarily unavailable. Please try again later.",
                        "error_code": "LLM_SERVER_ERROR",
                        "request_id": request_id
                    }
                )
            elif e.response.status_code == 400:
                logger.warning(
                    f"[{request_id}] LLM_VALIDATION: Gemini API validation error. "
                    f"Details: {str(e)}"
                )
                return JSONResponse(
                    status_code=400,
                    content={
                        "detail": "Invalid request to AI service. Please check your input.",
                        "error_code": "LLM_VALIDATION_ERROR",
                        "request_id": request_id
                    }
                )
            else:
                logger.error(
                    f"[{request_id}] LLM_UNKNOWN: Gemini API error {e.response.status_code}. "
                    f"Details: {str(e)}"
                )
                return JSONResponse(
                    status_code=503,
                    content={
                        "detail": "AI service error. Please try again.",
                        "error_code": "LLM_ERROR",
                        "request_id": request_id
                    }
                )
        
        except ValueError as e:
            # Validation errors (Day 74)
            logger.warning(
                f"[{request_id}] VALIDATION_ERROR: {str(e)} "
                f"at {request.url.path}"
            )
            return JSONResponse(
                status_code=400,
                content={
                    "detail": f"Invalid input: {str(e)}",
                    "error_code": "VALIDATION_ERROR",
                    "request_id": request_id
                }
            )
        
        except Exception as e:
            # Catch-all for unexpected errors (Day 74)
            error_type = type(e).__name__
            duration = time.time() - start_time
            
            logger.error(
                f"[{request_id}] UNEXPECTED_ERROR: {error_type} "
                f"at {request.url.path} after {duration:.2f}s. "
                f"Details: {str(e)}"
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "An unexpected error occurred. Our team has been notified.",
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "request_id": request_id
                }
            )


def handle_llm_error(error: Exception) -> tuple[int, dict]:
    """
    Convert LLM exception to HTTP response.
    
    Day 74 Feature: Standardized error handling for LLM operations
    
    Args:
        error: Exception from LLM call
        
    Returns:
        tuple: (status_code, error_dict)
    """
    error_str = str(error).lower()
    
    if "timeout" in error_str or "deadline" in error_str:
        return 504, {
            "detail": "AI service timeout. Please try again.",
            "error_code": "LLM_TIMEOUT"
        }
    elif "rate_limit" in error_str or "quota" in error_str or "429" in error_str:
        return 429, {
            "detail": "AI service rate limited. Try again in 1-2 minutes.",
            "error_code": "LLM_RATE_LIMIT"
        }
    elif "unauthorized" in error_str or "api_key" in error_str or "401" in error_str:
        logger.error(f"LLM API Key Error: {error}")
        return 500, {
            "detail": "API configuration error. Check service status.",
            "error_code": "LLM_AUTH_ERROR"
        }
    elif "500" in error_str or "server" in error_str:
        return 503, {
            "detail": "AI service unavailable. Try again later.",
            "error_code": "LLM_SERVER_ERROR"
        }
    else:
        return 503, {
            "detail": "AI service error. Please retry.",
            "error_code": "LLM_UNKNOWN_ERROR"
        }


def log_error_context(
    endpoint: str,
    error: Exception,
    input_length: int = 0,
    user_id: str = "unknown"
) -> None:
    """
    Log detailed error context for debugging.
    
    Day 74 Feature: Structured error logging with request details
    
    Args:
        endpoint: API endpoint where error occurred
        error: The exception
        input_length: Length of user input (for performance analysis)
        user_id: User identifier if available
    """
    logger.error(
        f"ERROR_CONTEXT: endpoint={endpoint}, "
        f"user={user_id}, "
        f"input_size={input_length}chars, "
        f"error_type={type(error).__name__}, "
        f"message={str(error)}"
    )
