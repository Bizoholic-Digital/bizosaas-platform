"""
Security and Authentication Module
Handles JWT tokens, password hashing, and authorization for the Business Directory service
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any, List
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import logging
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import get_db

# Configure logging
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security
security = HTTPBearer()

# Redis client for token blacklisting and rate limiting
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class SecurityManager:
    """
    Centralized security manager for authentication and authorization
    """
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against its hash"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
            "jti": secrets.token_urlsafe(32)  # Unique token ID
        })
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Token creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create access token"
            )
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32)
        })
        
        try:
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Refresh token creation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create refresh token"
            )
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check token type
            if payload.get("type") != token_type:
                raise JWTError("Invalid token type")
            
            # Check expiration
            exp = payload.get("exp")
            if exp is None or datetime.fromtimestamp(exp) < datetime.utcnow():
                raise JWTError("Token expired")
            
            return payload
            
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def is_token_blacklisted(self, jti: str) -> bool:
        """Check if token is blacklisted"""
        try:
            result = await redis_client.get(f"blacklisted_token:{jti}")
            return result is not None
        except Exception as e:
            logger.error(f"Redis blacklist check error: {e}")
            return False
    
    async def blacklist_token(self, jti: str, exp: int):
        """Add token to blacklist"""
        try:
            ttl = exp - int(datetime.utcnow().timestamp())
            if ttl > 0:
                await redis_client.setex(f"blacklisted_token:{jti}", ttl, "1")
        except Exception as e:
            logger.error(f"Redis blacklist error: {e}")
    
    def generate_api_key(self) -> str:
        """Generate secure API key"""
        return secrets.token_urlsafe(32)


# Global security manager
security_manager = SecurityManager()


class TokenData:
    """Token data structure"""
    def __init__(self, user_id: str, tenant_id: str, email: str, scopes: List[str]):
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.email = email
        self.scopes = scopes


class RateLimiter:
    """Rate limiting functionality"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
    
    async def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed under rate limit"""
        try:
            key = f"rate_limit:{identifier}"
            current = await redis_client.get(key)
            
            if current is None:
                await redis_client.setex(key, 60, 1)
                return True
            
            if int(current) >= self.requests_per_minute:
                return False
            
            await redis_client.incr(key)
            return True
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return True  # Allow request if rate limiting fails
    
    async def get_remaining_requests(self, identifier: str) -> int:
        """Get remaining requests for identifier"""
        try:
            key = f"rate_limit:{identifier}"
            current = await redis_client.get(key)
            if current is None:
                return self.requests_per_minute
            return max(0, self.requests_per_minute - int(current))
        except Exception:
            return self.requests_per_minute


# Rate limiter instances
general_rate_limiter = RateLimiter(settings.RATE_LIMIT_REQUESTS_PER_MINUTE)
search_rate_limiter = RateLimiter(settings.RATE_LIMIT_SEARCH_PER_MINUTE)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> TokenData:
    """
    FastAPI dependency to get current authenticated user
    """
    token = credentials.credentials
    
    # Verify token
    payload = security_manager.verify_token(token)
    
    # Check if token is blacklisted
    jti = payload.get("jti")
    if jti and await security_manager.is_token_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user information
    user_id = payload.get("sub")
    tenant_id = payload.get("tenant_id")
    email = payload.get("email")
    scopes = payload.get("scopes", [])
    
    if user_id is None or tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return TokenData(user_id=user_id, tenant_id=tenant_id, email=email, scopes=scopes)


async def get_current_active_user(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """
    FastAPI dependency to get current active user
    """
    # Additional checks can be added here (e.g., user is active, not suspended, etc.)
    return current_user


class RequireScopes:
    """
    Permission dependency for scope-based authorization
    """
    
    def __init__(self, required_scopes: List[str]):
        self.required_scopes = required_scopes
    
    def __call__(self, current_user: TokenData = Depends(get_current_active_user)) -> TokenData:
        """Check if user has required scopes"""
        if not self.required_scopes:
            return current_user
        
        user_scopes = set(current_user.scopes)
        required_scopes = set(self.required_scopes)
        
        if not required_scopes.issubset(user_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_scopes}"
            )
        
        return current_user


# Common permission dependencies
require_business_read = RequireScopes(["business:read"])
require_business_write = RequireScopes(["business:write"])
require_business_admin = RequireScopes(["business:admin"])
require_review_write = RequireScopes(["review:write"])
require_analytics_read = RequireScopes(["analytics:read"])


async def rate_limit_middleware(request: Request):
    """
    Rate limiting middleware
    """
    client_ip = request.client.host
    path = request.url.path
    
    # Choose appropriate rate limiter
    limiter = search_rate_limiter if "/search" in path else general_rate_limiter
    
    if not await limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            headers={
                "Retry-After": "60",
                "X-RateLimit-Limit": str(limiter.requests_per_minute),
                "X-RateLimit-Remaining": "0"
            }
        )
    
    # Add rate limit headers
    remaining = await limiter.get_remaining_requests(client_ip)
    request.state.rate_limit_remaining = remaining


class APIKeyAuth:
    """
    API Key authentication for external integrations
    """
    
    def __init__(self):
        self.api_key_header = "X-API-Key"
    
    async def __call__(self, request: Request) -> Optional[str]:
        """Validate API key from request headers"""
        api_key = request.headers.get(self.api_key_header)
        
        if not api_key:
            return None
        
        # Validate API key against database or cache
        # This would typically check against a tenant_api_keys table
        try:
            # For now, implement basic validation
            # In production, this should validate against database
            if len(api_key) >= 32:  # Basic length check
                return api_key
        except Exception as e:
            logger.error(f"API key validation error: {e}")
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


# API key authentication instance
api_key_auth = APIKeyAuth()


async def get_tenant_from_request(request: Request) -> str:
    """
    Extract tenant ID from request (headers, subdomain, etc.)
    """
    # Try header first
    tenant_id = request.headers.get("X-Tenant-ID")
    if tenant_id:
        return tenant_id
    
    # Try subdomain extraction
    host = request.headers.get("host", "")
    if "." in host:
        subdomain = host.split(".")[0]
        if subdomain not in ["www", "api", "admin"]:
            return subdomain
    
    # Default tenant for development
    if settings.is_development:
        return "default"
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Tenant ID required"
    )


class TenantSecurity:
    """
    Tenant-specific security validations
    """
    
    @staticmethod
    async def validate_tenant_access(user_tenant_id: str, resource_tenant_id: str):
        """Validate user can access tenant resource"""
        if user_tenant_id != resource_tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to tenant resource"
            )
    
    @staticmethod
    async def get_user_tenant_permissions(user_id: str, tenant_id: str) -> List[str]:
        """Get user permissions within a tenant"""
        # This would typically query the database for user-tenant permissions
        # For now, return basic permissions
        return ["business:read", "business:write", "review:write"]


# Security utilities
def generate_secure_filename(filename: str) -> str:
    """Generate secure filename for uploads"""
    import uuid
    from pathlib import Path
    
    # Get file extension
    suffix = Path(filename).suffix.lower()
    
    # Generate UUID-based filename
    secure_name = f"{uuid.uuid4().hex}{suffix}"
    return secure_name


def validate_file_type(content_type: str, allowed_types: List[str]) -> bool:
    """Validate file content type"""
    return content_type.lower() in [t.lower() for t in allowed_types]


async def cleanup_security():
    """Cleanup security resources"""
    try:
        await redis_client.close()
        logger.info("Security cleanup completed")
    except Exception as e:
        logger.error(f"Security cleanup error: {e}")


# Health check for security components
async def check_security_health() -> dict:
    """Check security component health"""
    health = {
        "redis": "unhealthy",
        "rate_limiting": False,
        "token_validation": False
    }
    
    try:
        # Check Redis connectivity
        await redis_client.ping()
        health["redis"] = "healthy"
        health["rate_limiting"] = True
        
        # Test token creation/validation
        test_token = security_manager.create_access_token({"sub": "test", "tenant_id": "test"})
        security_manager.verify_token(test_token)
        health["token_validation"] = True
        
    except Exception as e:
        logger.error(f"Security health check error: {e}")
        health["error"] = str(e)
    
    return health