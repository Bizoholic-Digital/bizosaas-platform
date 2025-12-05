#!/usr/bin/env python3
"""
Authentication Middleware for BizOSaaS Platform Integration
Provides seamless authentication integration for other services
"""

import asyncio
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Callable, Union
from functools import wraps

from fastapi import Request, Response, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import httpx
import structlog
from jose import JWTError, jwt
import redis.asyncio as redis

from auth_client import AuthClient, AuthError

logger = structlog.get_logger()


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware for BizOSaaS platform services
    Validates JWT tokens and injects user context
    """
    
    def __init__(
        self,
        app,
        auth_service_url: str = "http://localhost:8007",
        secret_key: str = "your-secret-key",
        excluded_paths: List[str] = None,
        platform_name: str = "bizosaas",
        cache_ttl: int = 300  # 5 minutes
    ):
        super().__init__(app)
        self.auth_service_url = auth_service_url.rstrip("/")
        self.secret_key = secret_key
        self.platform_name = platform_name
        self.cache_ttl = cache_ttl
        
        # Default excluded paths (no auth required)
        self.excluded_paths = excluded_paths or [
            "/health",
            "/metrics",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico"
        ]
        
        # Redis cache for user sessions
        self.redis_client = None
        self.auth_client = None
    
    async def setup_clients(self):
        """Initialize Redis and HTTP clients"""
        if not self.redis_client:
            try:
                self.redis_client = redis.from_url("redis://host.docker.internal:6379/1")
                await self.redis_client.ping()
            except Exception as e:
                logger.warning("Failed to connect to Redis, using memory cache", error=str(e))
                self.redis_client = None
        
        if not self.auth_client:
            self.auth_client = AuthClient(base_url=self.auth_service_url)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Main middleware dispatch"""
        await self.setup_clients()
        
        # Skip authentication for excluded paths
        if any(request.url.path.startswith(path) for path in self.excluded_paths):
            return await call_next(request)
        
        # Extract and validate token
        try:
            user_info = await self.authenticate_request(request)
            
            # Inject user context into request state
            if user_info:
                request.state.user = user_info
                request.state.authenticated = True
                request.state.tenant_id = user_info.get("tenant_id")
                request.state.user_role = user_info.get("role")
                request.state.platform_access = user_info.get("allowed_platforms", [])
            else:
                request.state.authenticated = False
                
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
        except Exception as e:
            logger.error(
                "Authentication middleware error",
                error=str(e),
                path=request.url.path
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Authentication service error"}
            )
        
        # Verify platform access
        if request.state.authenticated and not self.has_platform_access(request.state.user):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Access denied to platform: {self.platform_name}"}
            )
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response
    
    async def authenticate_request(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate request and return user info"""
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Check for session cookie as fallback
            session_token = request.cookies.get("bizosaas_auth")
            if not session_token:
                return None
            token = session_token
        else:
            token = auth_header[7:]  # Remove "Bearer " prefix
        
        # Try cache first
        cached_user = await self.get_cached_user(token)
        if cached_user:
            return cached_user
        
        # Validate token locally first
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"],
                options={"verify_exp": True}
            )
            
            user_info = {
                "id": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "tenant_id": payload.get("tenant_id"),
                "platform": payload.get("platform"),
                "session_id": payload.get("session_id"),
                "allowed_platforms": payload.get("allowed_platforms", []),
                "exp": payload.get("exp")
            }
            
            # Cache the user info
            await self.cache_user(token, user_info)
            
            return user_info
            
        except JWTError as e:
            logger.warning("Invalid JWT token", error=str(e))
            # Try remote validation as fallback
            return await self.validate_token_remote(token)
    
    async def validate_token_remote(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate token against auth service"""
        try:
            if not self.auth_client:
                return None
            
            # Use token to get user info from auth service
            self.auth_client._access_token = token
            user_response = await self.auth_client.get_current_user()
            
            user_info = {
                "id": user_response["user"]["id"],
                "email": user_response["user"]["email"],
                "role": user_response["user"]["role"],
                "tenant_id": user_response["user"]["tenant_id"],
                "allowed_platforms": user_response["user"].get("allowed_platforms", []),
                "permissions": user_response.get("permissions", [])
            }\n            \n            # Cache the validated user\n            await self.cache_user(token, user_info)\n            \n            return user_info\n            \n        except Exception as e:\n            logger.warning(\"Remote token validation failed\", error=str(e))\n            return None\n    \n    async def get_cached_user(self, token: str) -> Optional[Dict[str, Any]]:\n        \"\"\"Get user info from cache\"\"\"\n        if not self.redis_client:\n            return None\n        \n        try:\n            cache_key = f\"auth_token:{token[:20]}\"  # Use token prefix as key\n            cached = await self.redis_client.get(cache_key)\n            \n            if cached:\n                import json\n                user_info = json.loads(cached)\n                \n                # Check if cached token is still valid\n                if user_info.get(\"exp\", 0) > time.time():\n                    return user_info\n                else:\n                    # Remove expired token from cache\n                    await self.redis_client.delete(cache_key)\n            \n            return None\n            \n        except Exception as e:\n            logger.warning(\"Failed to get cached user\", error=str(e))\n            return None\n    \n    async def cache_user(self, token: str, user_info: Dict[str, Any]):\n        \"\"\"Cache user info\"\"\"\n        if not self.redis_client:\n            return\n        \n        try:\n            cache_key = f\"auth_token:{token[:20]}\"\n            import json\n            await self.redis_client.setex(\n                cache_key,\n                self.cache_ttl,\n                json.dumps(user_info, default=str)\n            )\n        except Exception as e:\n            logger.warning(\"Failed to cache user\", error=str(e))\n    \n    def has_platform_access(self, user_info: Dict[str, Any]) -> bool:\n        \"\"\"Check if user has access to current platform\"\"\"\n        if user_info.get(\"role\") == \"super_admin\":\n            return True\n        \n        allowed_platforms = user_info.get(\"allowed_platforms\", [])\n        return self.platform_name in allowed_platforms\n\n\n# Dependency injection helpers\nsecurity = HTTPBearer(auto_error=False)\n\n\nasync def get_current_user(\n    request: Request,\n    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)\n) -> Optional[Dict[str, Any]]:\n    \"\"\"Get current authenticated user from request state\"\"\"\n    return getattr(request.state, \"user\", None)\n\n\nasync def require_authentication(\n    request: Request,\n    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)\n) -> Dict[str, Any]:\n    \"\"\"Require authentication - raise error if not authenticated\"\"\"\n    if not getattr(request.state, \"authenticated\", False):\n        raise HTTPException(\n            status_code=status.HTTP_401_UNAUTHORIZED,\n            detail=\"Authentication required\",\n            headers={\"WWW-Authenticate\": \"Bearer\"}\n        )\n    \n    return request.state.user\n\n\ndef require_role(required_roles: Union[str, List[str]]):\n    \"\"\"Dependency to require specific user roles\"\"\"\n    if isinstance(required_roles, str):\n        required_roles = [required_roles]\n    \n    async def role_checker(request: Request) -> Dict[str, Any]:\n        user = await require_authentication(request)\n        \n        user_role = user.get(\"role\")\n        if user_role not in required_roles and user_role != \"super_admin\":\n            raise HTTPException(\n                status_code=status.HTTP_403_FORBIDDEN,\n                detail=f\"Required roles: {required_roles}\"\n            )\n        \n        return user\n    \n    return role_checker\n\n\ndef require_platform_access(platforms: Union[str, List[str]]):\n    \"\"\"Dependency to require access to specific platforms\"\"\"\n    if isinstance(platforms, str):\n        platforms = [platforms]\n    \n    async def platform_checker(request: Request) -> Dict[str, Any]:\n        user = await require_authentication(request)\n        \n        user_role = user.get(\"role\")\n        allowed_platforms = user.get(\"allowed_platforms\", [])\n        \n        if user_role == \"super_admin\":\n            return user\n        \n        if not any(platform in allowed_platforms for platform in platforms):\n            raise HTTPException(\n                status_code=status.HTTP_403_FORBIDDEN,\n                detail=f\"Access denied to platforms: {platforms}\"\n            )\n        \n        return user\n    \n    return platform_checker\n\n\n# Decorators for function-level authentication\ndef authenticated(func):\n    \"\"\"Decorator to require authentication for a function\"\"\"\n    @wraps(func)\n    async def wrapper(*args, **kwargs):\n        # Find request object in args/kwargs\n        request = None\n        for arg in args:\n            if isinstance(arg, Request):\n                request = arg\n                break\n        \n        if not request:\n            request = kwargs.get(\"request\")\n        \n        if not request or not getattr(request.state, \"authenticated\", False):\n            raise HTTPException(\n                status_code=status.HTTP_401_UNAUTHORIZED,\n                detail=\"Authentication required\"\n            )\n        \n        return await func(*args, **kwargs)\n    \n    return wrapper\n\n\ndef require_role_decorator(roles: Union[str, List[str]]):\n    \"\"\"Decorator to require specific roles\"\"\"\n    if isinstance(roles, str):\n        roles = [roles]\n    \n    def decorator(func):\n        @wraps(func)\n        async def wrapper(*args, **kwargs):\n            # Find request object\n            request = None\n            for arg in args:\n                if isinstance(arg, Request):\n                    request = arg\n                    break\n            \n            if not request:\n                request = kwargs.get(\"request\")\n            \n            if not request or not getattr(request.state, \"authenticated\", False):\n                raise HTTPException(\n                    status_code=status.HTTP_401_UNAUTHORIZED,\n                    detail=\"Authentication required\"\n                )\n            \n            user_role = request.state.user.get(\"role\")\n            if user_role not in roles and user_role != \"super_admin\":\n                raise HTTPException(\n                    status_code=status.HTTP_403_FORBIDDEN,\n                    detail=f\"Required roles: {roles}\"\n                )\n            \n            return await func(*args, **kwargs)\n        \n        return wrapper\n    \n    return decorator\n\n\n# Rate limiting middleware\nclass RateLimitMiddleware(BaseHTTPMiddleware):\n    \"\"\"Rate limiting middleware with Redis backend\"\"\"\n    \n    def __init__(self, app, redis_url: str = \"redis://host.docker.internal:6379/2\"):\n        super().__init__(app)\n        self.redis_client = None\n        self.redis_url = redis_url\n    \n    async def setup_redis(self):\n        \"\"\"Setup Redis connection\"\"\"\n        if not self.redis_client:\n            try:\n                self.redis_client = redis.from_url(self.redis_url)\n                await self.redis_client.ping()\n            except Exception as e:\n                logger.warning(\"Failed to connect to Redis for rate limiting\", error=str(e))\n    \n    async def dispatch(self, request: Request, call_next: Callable) -> Response:\n        \"\"\"Rate limit dispatch\"\"\"\n        await self.setup_redis()\n        \n        if not self.redis_client:\n            return await call_next(request)\n        \n        # Get client identifier\n        client_id = self.get_client_id(request)\n        \n        # Check rate limit\n        if await self.is_rate_limited(client_id):\n            return JSONResponse(\n                status_code=status.HTTP_429_TOO_MANY_REQUESTS,\n                content={\"detail\": \"Rate limit exceeded\"},\n                headers={\"Retry-After\": \"60\"}\n            )\n        \n        # Record request\n        await self.record_request(client_id)\n        \n        return await call_next(request)\n    \n    def get_client_id(self, request: Request) -> str:\n        \"\"\"Get client identifier for rate limiting\"\"\"\n        # Use authenticated user ID if available\n        if getattr(request.state, \"authenticated\", False):\n            user_info = getattr(request.state, \"user\", {})\n            return f\"user:{user_info.get('id', 'unknown')}\"\n        \n        # Use IP address as fallback\n        forwarded_for = request.headers.get(\"X-Forwarded-For\")\n        if forwarded_for:\n            ip = forwarded_for.split(\",\")[0].strip()\n        else:\n            ip = request.client.host if request.client else \"unknown\"\n        \n        return f\"ip:{ip}\"\n    \n    async def is_rate_limited(self, client_id: str, limit: int = 60, window: int = 60) -> bool:\n        \"\"\"Check if client is rate limited\"\"\"\n        try:\n            current_time = int(time.time())\n            window_start = current_time - window\n            \n            # Clean old entries\n            await self.redis_client.zremrangebyscore(\n                f\"rate_limit:{client_id}\",\n                0,\n                window_start\n            )\n            \n            # Count requests in current window\n            request_count = await self.redis_client.zcard(f\"rate_limit:{client_id}\")\n            \n            return request_count >= limit\n            \n        except Exception as e:\n            logger.warning(\"Rate limit check failed\", error=str(e))\n            return False\n    \n    async def record_request(self, client_id: str, window: int = 60):\n        \"\"\"Record a request for rate limiting\"\"\"\n        try:\n            current_time = int(time.time())\n            \n            # Add current request\n            await self.redis_client.zadd(\n                f\"rate_limit:{client_id}\",\n                {str(uuid.uuid4()): current_time}\n            )\n            \n            # Set expiration\n            await self.redis_client.expire(f\"rate_limit:{client_id}\", window * 2)\n            \n        except Exception as e:\n            logger.warning(\"Failed to record request\", error=str(e))\n\n\n# Session management utilities\nclass SessionManager:\n    \"\"\"Manage user sessions across the platform\"\"\"\n    \n    def __init__(self, redis_url: str = \"redis://host.docker.internal:6379/3\"):\n        self.redis_client = None\n        self.redis_url = redis_url\n    \n    async def setup_redis(self):\n        \"\"\"Setup Redis connection\"\"\"\n        if not self.redis_client:\n            self.redis_client = redis.from_url(self.redis_url)\n    \n    async def create_session(\n        self,\n        user_id: str,\n        tenant_id: str,\n        platform: str,\n        session_data: Dict[str, Any] = None\n    ) -> str:\n        \"\"\"Create a new session\"\"\"\n        await self.setup_redis()\n        \n        session_id = str(uuid.uuid4())\n        session_key = f\"session:{session_id}\"\n        \n        session_info = {\n            \"user_id\": user_id,\n            \"tenant_id\": tenant_id,\n            \"platform\": platform,\n            \"created_at\": datetime.now(timezone.utc).isoformat(),\n            \"last_accessed\": datetime.now(timezone.utc).isoformat(),\n            \"data\": session_data or {}\n        }\n        \n        import json\n        await self.redis_client.setex(\n            session_key,\n            3600 * 24,  # 24 hours\n            json.dumps(session_info, default=str)\n        )\n        \n        return session_id\n    \n    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:\n        \"\"\"Get session information\"\"\"\n        await self.setup_redis()\n        \n        session_key = f\"session:{session_id}\"\n        session_data = await self.redis_client.get(session_key)\n        \n        if session_data:\n            import json\n            session_info = json.loads(session_data)\n            \n            # Update last accessed time\n            session_info[\"last_accessed\"] = datetime.now(timezone.utc).isoformat()\n            await self.redis_client.setex(\n                session_key,\n                3600 * 24,\n                json.dumps(session_info, default=str)\n            )\n            \n            return session_info\n        \n        return None\n    \n    async def invalidate_session(self, session_id: str):\n        \"\"\"Invalidate a session\"\"\"\n        await self.setup_redis()\n        \n        session_key = f\"session:{session_id}\"\n        await self.redis_client.delete(session_key)\n    \n    async def invalidate_user_sessions(self, user_id: str):\n        \"\"\"Invalidate all sessions for a user\"\"\"\n        await self.setup_redis()\n        \n        # This is a simplified implementation\n        # In production, you'd want to maintain a user -> sessions mapping\n        pattern = \"session:*\"\n        async for key in self.redis_client.scan_iter(match=pattern):\n            session_data = await self.redis_client.get(key)\n            if session_data:\n                import json\n                session_info = json.loads(session_data)\n                if session_info.get(\"user_id\") == user_id:\n                    await self.redis_client.delete(key)\n\n\n# Integration helpers\ndef setup_auth_middleware(\n    app,\n    auth_service_url: str = \"http://localhost:8007\",\n    secret_key: str = \"your-secret-key\",\n    platform_name: str = \"bizosaas\",\n    excluded_paths: List[str] = None,\n    enable_rate_limiting: bool = True\n):\n    \"\"\"Setup authentication middleware for a FastAPI app\"\"\"\n    \n    # Add authentication middleware\n    app.add_middleware(\n        AuthenticationMiddleware,\n        auth_service_url=auth_service_url,\n        secret_key=secret_key,\n        platform_name=platform_name,\n        excluded_paths=excluded_paths\n    )\n    \n    # Add rate limiting middleware\n    if enable_rate_limiting:\n        app.add_middleware(RateLimitMiddleware)\n\n\n# Example usage\nif __name__ == \"__main__\":\n    from fastapi import FastAPI\n    \n    app = FastAPI()\n    \n    # Setup authentication\n    setup_auth_middleware(\n        app,\n        auth_service_url=\"http://localhost:8007\",\n        secret_key=\"your-secret-key\",\n        platform_name=\"bizosaas\"\n    )\n    \n    @app.get(\"/protected\")\n    async def protected_endpoint(user: Dict[str, Any] = Depends(require_authentication)):\n        return {\"message\": f\"Hello {user['email']}\", \"user_id\": user[\"id\"]}\n    \n    @app.get(\"/admin-only\")\n    async def admin_endpoint(user: Dict[str, Any] = Depends(require_role([\"admin\", \"super_admin\"]))):\n        return {\"message\": \"Admin access granted\", \"user\": user}