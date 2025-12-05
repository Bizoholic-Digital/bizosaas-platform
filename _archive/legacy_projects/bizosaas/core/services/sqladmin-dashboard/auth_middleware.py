"""
Authentication Middleware for SQLAdmin Dashboard
Integrates with unified auth system at localhost:3002
"""

import aiohttp
import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from fastapi import Request, HTTPException, status
from pydantic import BaseModel
import os

# Configure logging
logger = logging.getLogger(__name__)

# Configuration
UNIFIED_AUTH_URL = os.getenv("UNIFIED_AUTH_URL", "http://host.docker.internal:3002")
UNIFIED_AUTH_BROWSER_URL = os.getenv("UNIFIED_AUTH_BROWSER_URL", "http://localhost:3002")
AUTH_TIMEOUT = float(os.getenv("AUTH_TIMEOUT", "5.0"))

class UserSession(BaseModel):
    """User session data model"""
    user_id: str
    email: str
    role: str
    permissions: List[str]
    tenant_id: Optional[str] = None
    tenant_name: Optional[str] = None
    is_super_admin: bool = False
    last_activity: Optional[datetime] = None

class AuthenticationError(Exception):
    """Custom authentication error"""
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class AuthMiddleware:
    """Authentication middleware for SQLAdmin dashboard"""
    
    def __init__(self):
        self.session_cache = {}  # Simple in-memory cache for sessions
        self.cache_timeout = 300  # 5 minutes cache
    
    async def verify_session_with_unified_auth(self, request: Request) -> Optional[UserSession]:
        """
        Verify session with the unified auth system at localhost:3002
        Returns UserSession if valid, None if invalid
        """
        try:
            # Extract session token from multiple sources
            session_token = await self._extract_session_token(request)
            
            if not session_token:
                logger.debug("No session token found in request")
                return None
            
            # Check cache first
            cached_session = self._get_cached_session(session_token)
            if cached_session:
                logger.debug(f"Using cached session for token: {session_token[:10]}...")
                return cached_session
            
            # Verify with unified auth system
            session_data = await self._verify_with_auth_service(session_token)
            
            if session_data:
                user_session = self._create_user_session(session_data)
                # Cache the session
                self._cache_session(session_token, user_session)
                logger.info(f"Session verified for user: {user_session.email}")
                return user_session
            
            logger.warning("Session verification failed")
            return None
            
        except Exception as e:
            logger.error(f"Session verification error: {e}")
            return None
    
    async def _extract_session_token(self, request: Request) -> Optional[str]:
        """Extract session token from request cookies or headers"""
        # Try cookies first
        session_token = (
            request.cookies.get("session_token") or 
            request.cookies.get("auth_token") or
            request.cookies.get("access_token")
        )
        
        if session_token:
            return session_token
        
        # Try Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header:
            if auth_header.startswith("Bearer "):
                return auth_header[7:]
            elif auth_header.startswith("Token "):
                return auth_header[6:]
        
        # Try custom headers
        return (
            request.headers.get("X-Session-Token") or
            request.headers.get("X-Auth-Token")
        )
    
    async def _verify_with_auth_service(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Verify session token with the unified auth service"""
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=AUTH_TIMEOUT)
            ) as session:
                
                # Prepare headers
                headers = {
                    "Authorization": f"Bearer {session_token}",
                    "Content-Type": "application/json",
                    "User-Agent": "SQLAdmin-Dashboard/1.0"
                }
                
                # Try different auth endpoints
                auth_endpoints = [
                    f"{UNIFIED_AUTH_URL}/api/auth/verify",
                    f"{UNIFIED_AUTH_URL}/auth/me",
                    f"{UNIFIED_AUTH_URL}/api/auth/me"
                ]
                
                for endpoint in auth_endpoints:
                    try:
                        async with session.get(endpoint, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                logger.debug(f"Auth success from endpoint: {endpoint}")
                                return data
                            elif response.status == 401:
                                logger.debug(f"Unauthorized from endpoint: {endpoint}")
                            else:
                                logger.debug(f"Auth endpoint {endpoint} returned {response.status}")
                    except aiohttp.ClientError as e:
                        logger.debug(f"Error contacting {endpoint}: {e}")
                        continue
                
                return None
                
        except asyncio.TimeoutError:
            logger.warning("Auth service timeout")
            return None
        except Exception as e:
            logger.error(f"Auth service error: {e}")
            return None
    
    def _create_user_session(self, session_data: Dict[str, Any]) -> UserSession:
        """Create UserSession object from auth service response"""
        # Handle different response formats
        user_data = session_data.get("user", session_data)
        
        # Extract user information
        user_id = str(user_data.get("id", user_data.get("user_id", "unknown")))
        email = user_data.get("email", "unknown")
        role = user_data.get("role", "client")
        
        # Extract permissions
        permissions = user_data.get("permissions", [])
        if isinstance(permissions, dict):
            permissions = list(permissions.keys())
        elif not isinstance(permissions, list):
            permissions = []
        
        # Extract tenant information
        tenant_info = session_data.get("tenant", {})
        tenant_id = tenant_info.get("id") or user_data.get("tenant_id")
        tenant_name = tenant_info.get("name") or tenant_info.get("slug", "Unknown")
        
        # Determine if super admin
        is_super_admin = (
            role.upper() in ["SUPER_ADMIN", "SUPERUSER"] or
            "super_admin" in permissions or
            user_data.get("is_superuser", False)
        )
        
        return UserSession(
            user_id=user_id,
            email=email,
            role=role,
            permissions=permissions,
            tenant_id=str(tenant_id) if tenant_id else None,
            tenant_name=tenant_name,
            is_super_admin=is_super_admin,
            last_activity=datetime.now(timezone.utc)
        )
    
    def _get_cached_session(self, session_token: str) -> Optional[UserSession]:
        """Get session from cache if valid"""
        cache_key = f"session:{session_token}"
        cached_data = self.session_cache.get(cache_key)
        
        if cached_data:
            session, timestamp = cached_data
            # Check if cache is still valid
            if (datetime.now(timezone.utc) - timestamp).total_seconds() < self.cache_timeout:
                return session
            else:
                # Remove expired cache
                del self.session_cache[cache_key]
        
        return None
    
    def _cache_session(self, session_token: str, user_session: UserSession):
        """Cache session data"""
        cache_key = f"session:{session_token}"
        self.session_cache[cache_key] = (user_session, datetime.now(timezone.utc))
        
        # Simple cache cleanup - remove old entries
        if len(self.session_cache) > 1000:  # Limit cache size
            oldest_keys = sorted(
                self.session_cache.keys(),
                key=lambda k: self.session_cache[k][1]
            )[:100]
            for key in oldest_keys:
                del self.session_cache[key]
    
    async def require_authentication(self, request: Request) -> UserSession:
        """Dependency function to require authentication"""
        user_session = await self.verify_session_with_unified_auth(request)
        
        if not user_session:
            raise AuthenticationError(
                "Authentication required",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        return user_session
    
    async def require_super_admin(self, request: Request) -> UserSession:
        """Dependency function to require SUPER_ADMIN role"""
        user_session = await self.require_authentication(request)
        
        if not user_session.is_super_admin and user_session.role.upper() not in ["SUPER_ADMIN", "SUPERUSER"]:
            raise AuthenticationError(
                "SUPER_ADMIN access required for infrastructure management",
                status_code=status.HTTP_403_FORBIDDEN
            )
        
        return user_session
    
    def clear_cache(self):
        """Clear the session cache"""
        self.session_cache.clear()
        logger.info("Session cache cleared")

# Global instance
auth_middleware = AuthMiddleware()

# Convenience functions
async def verify_session(request: Request) -> Optional[UserSession]:
    """Verify user session"""
    return await auth_middleware.verify_session_with_unified_auth(request)

async def require_authentication(request: Request) -> UserSession:
    """Require authentication"""
    return await auth_middleware.require_authentication(request)

async def require_super_admin(request: Request) -> UserSession:
    """Require super admin access"""
    return await auth_middleware.require_super_admin(request)

def get_login_redirect_url(return_url: str = "http://localhost:5000") -> str:
    """Get the login redirect URL"""
    return f"{UNIFIED_AUTH_BROWSER_URL}/auth/login/?redirect={return_url}"

def get_logout_url() -> str:
    """Get the logout URL"""
    return f"{UNIFIED_AUTH_BROWSER_URL}/auth/logout"