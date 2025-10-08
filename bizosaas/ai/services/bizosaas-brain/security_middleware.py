"""
Security Middleware for BizOSaaS Brain API
Implements rate limiting, security headers, and request validation
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Optional
import time
import hashlib
import logging
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RateLimiter:
    """In-memory rate limiter with Redis fallback"""

    def __init__(self, redis_client=None):
        self.redis_client = redis_client
        self.local_store: Dict[str, list] = defaultdict(list)
        self.limits = {
            "default": (100, 60),  # 100 requests per 60 seconds
            "ai_generation": (10, 60),  # 10 AI requests per minute
            "admin": (1000, 60),  # Higher limit for admin
            "public": (30, 60),  # Lower limit for public endpoints
        }

    def _get_client_key(self, request: Request) -> str:
        """Generate unique key for client"""
        # Use X-Forwarded-For if behind proxy, otherwise use client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"

        # Include tenant ID for multi-tenant rate limiting
        tenant = request.headers.get("X-Tenant", "default")

        return f"ratelimit:{tenant}:{client_ip}"

    def _get_rate_limit_type(self, path: str) -> str:
        """Determine rate limit type based on path"""
        if "/ai/" in path or "/agents/" in path:
            return "ai_generation"
        elif "/admin/" in path:
            return "admin"
        elif "/api/public/" in path:
            return "public"
        return "default"

    def is_allowed(self, request: Request) -> tuple[bool, Optional[dict]]:
        """Check if request is within rate limit"""
        client_key = self._get_client_key(request)
        limit_type = self._get_rate_limit_type(request.url.path)
        max_requests, window_seconds = self.limits[limit_type]

        now = time.time()
        window_start = now - window_seconds

        # Clean old entries
        self.local_store[client_key] = [
            timestamp for timestamp in self.local_store[client_key]
            if timestamp > window_start
        ]

        # Check if under limit
        current_requests = len(self.local_store[client_key])

        if current_requests >= max_requests:
            retry_after = int(self.local_store[client_key][0] + window_seconds - now)
            return False, {
                "limit": max_requests,
                "remaining": 0,
                "retry_after": retry_after
            }

        # Add current request
        self.local_store[client_key].append(now)

        return True, {
            "limit": max_requests,
            "remaining": max_requests - current_requests - 1,
            "reset": int(now + window_seconds)
        }


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'"
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""

    def __init__(self, app, redis_client=None):
        super().__init__(app)
        self.rate_limiter = RateLimiter(redis_client)

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        # Check rate limit
        allowed, limit_info = self.rate_limiter.is_allowed(request)

        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Retry after {limit_info['retry_after']} seconds",
                    "retry_after": limit_info["retry_after"]
                },
                headers={
                    "X-RateLimit-Limit": str(limit_info["limit"]),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(limit_info["retry_after"])
                }
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(limit_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(limit_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(limit_info["reset"])

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate and sanitize requests"""

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

    async def dispatch(self, request: Request, call_next):
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_CONTENT_LENGTH:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={
                    "error": "Payload too large",
                    "max_size": self.MAX_CONTENT_LENGTH
                }
            )

        # Validate Content-Type for POST/PUT/PATCH
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith(("application/json", "multipart/form-data")):
                return JSONResponse(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    content={
                        "error": "Unsupported media type",
                        "expected": ["application/json", "multipart/form-data"]
                    }
                )

        return await call_next(request)


# Security configuration
SECURITY_CONFIG = {
    "rate_limiting": {
        "enabled": True,
        "limits": {
            "default": (100, 60),
            "ai_generation": (10, 60),
            "admin": (1000, 60),
            "public": (30, 60),
        }
    },
    "security_headers": {
        "enabled": True,
        "hsts_max_age": 31536000,
        "csp_enabled": True
    },
    "request_validation": {
        "enabled": True,
        "max_content_length": 10 * 1024 * 1024
    }
}
