#!/usr/bin/env python3
"""
BizOSaaS Authentication Client
Production-ready API client for interacting with the auth service
Includes retry logic, circuit breaker, and comprehensive error handling
"""

import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, asdict
from enum import Enum
import httpx
import structlog

logger = structlog.get_logger()


class AuthError(Exception):
    """Base authentication error"""
    pass


class RateLimitError(AuthError):
    """Rate limit exceeded"""
    pass


class NetworkError(AuthError):
    """Network communication error"""
    pass


class CircuitOpenException(AuthError):
    """Circuit breaker is open"""
    pass


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    USER = "user"
    READONLY = "readonly"
    AGENT = "agent"
    SERVICE_ACCOUNT = "service_account"


@dataclass
class User:
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"
    tenant_id: Optional[str] = None
    allowed_platforms: List[str] = None
    is_active: bool = True
    is_verified: bool = False
    
    def __post_init__(self):
        if self.allowed_platforms is None:
            self.allowed_platforms = []


@dataclass
class Tenant:
    id: str
    name: str
    slug: str
    status: str
    allowed_platforms: List[str]
    max_users: int = 10
    domain: Optional[str] = None
    subscription_plan: Optional[str] = None


@dataclass
class AuthResponse:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: User
    tenant: Tenant
    permissions: List[str]


@dataclass
class LoginRequest:
    email: str
    password: str
    platform: str = "bizosaas"
    remember_me: bool = False
    device_fingerprint: Optional[str] = None


class CircuitBreaker:
    """Circuit breaker pattern for resilient API calls"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenException("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == 'HALF_OPEN':
                self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise
    
    def record_failure(self):
        """Record a failure and potentially open the circuit"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
    
    def reset(self):
        """Reset the circuit breaker"""
        self.failure_count = 0
        self.state = 'CLOSED'


class AuthClient:
    """Production-ready authentication client with retry logic and circuit breaker"""
    
    def __init__(
        self,
        base_url: str = "http://localhost:8007",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_retry_delay = max_retry_delay
        
        # Circuit breaker for reliability
        self.circuit_breaker = CircuitBreaker()
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100),
            headers={
                "User-Agent": "BizOSaaS-AuthClient/1.0",
                "Content-Type": "application/json"
            }
        )
        
        # Authentication state
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers if token is available"""
        headers = {}
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        return headers
    
    async def _retry_with_exponential_backoff(self, func, *args, **kwargs):
        """Execute function with exponential backoff retry logic"""
        last_exception = None
        delay = self.retry_delay
        
        for attempt in range(self.max_retries + 1):
            try:
                return await self.circuit_breaker.call(func, *args, **kwargs)
            except (httpx.TimeoutException, httpx.ConnectError, httpx.ReadError) as e:
                last_exception = NetworkError(f"Network error: {str(e)}")
                
                if attempt == self.max_retries:
                    break
                
                # Add jitter to prevent thundering herd
                jittered_delay = delay * (0.5 + 0.5 * time.time() % 1)
                await asyncio.sleep(min(jittered_delay, self.max_retry_delay))
                delay *= 2
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    # Rate limited, use longer delay
                    retry_after = int(e.response.headers.get("Retry-After", 60))
                    await asyncio.sleep(retry_after)
                    last_exception = RateLimitError("Rate limit exceeded")
                    continue
                elif e.response.status_code >= 500:
                    # Server error, retry
                    last_exception = NetworkError(f"Server error: {e.response.status_code}")
                    if attempt < self.max_retries:
                        await asyncio.sleep(delay)
                        delay *= 2
                        continue
                
                # Client error (4xx), don't retry
                raise AuthError(f"Authentication error: {e.response.status_code}")
            except CircuitOpenException:
                raise
            except Exception as e:
                last_exception = AuthError(f"Unexpected error: {str(e)}")
                break
        
        if last_exception:
            raise last_exception
        
        raise AuthError("Max retries exceeded")
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        include_auth: bool = True
    ) -> Dict[str, Any]:
        """Make authenticated HTTP request with retry logic"""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_auth_headers() if include_auth else {}
        
        async def _request():
            if method.upper() == "GET":
                response = await self.client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = await self.client.post(url, json=data, params=params, headers=headers)
            elif method.upper() == "PUT":
                response = await self.client.put(url, json=data, params=params, headers=headers)
            elif method.upper() == "DELETE":
                response = await self.client.delete(url, params=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {}
            
            return response.json()
        
        return await self._retry_with_exponential_backoff(_request)
    
    async def login(self, login_request: Union[LoginRequest, Dict[str, Any]]) -> AuthResponse:
        """Authenticate user and store tokens"""
        try:
            if isinstance(login_request, LoginRequest):
                data = asdict(login_request)
            else:
                data = login_request
            
            response_data = await self._make_request(
                "POST", 
                "/auth/sso/login", 
                data=data,
                include_auth=False
            )
            
            # Store tokens
            self._access_token = response_data["access_token"]
            self._refresh_token = response_data["refresh_token"]
            
            # Calculate token expiration
            expires_in = response_data.get("expires_in", 1800)  # Default 30 minutes
            self._token_expires_at = datetime.now(timezone.utc).timestamp() + expires_in
            
            # Create response objects
            user_data = response_data["user"]
            user = User(
                id=user_data["id"],
                email=user_data["email"],
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                role=user_data.get("role", "user"),
                tenant_id=user_data.get("tenant_id"),
                allowed_platforms=user_data.get("allowed_platforms", []),
                is_active=user_data.get("is_active", True),
                is_verified=user_data.get("is_verified", False)
            )
            
            tenant_data = response_data["tenant"]
            tenant = Tenant(
                id=tenant_data["id"],
                name=tenant_data["name"],
                slug=tenant_data["slug"],
                status=tenant_data["status"],
                allowed_platforms=tenant_data["allowed_platforms"],
                max_users=tenant_data.get("max_users", 10),
                domain=tenant_data.get("domain"),
                subscription_plan=tenant_data.get("subscription_plan")
            )
            
            auth_response = AuthResponse(
                access_token=response_data["access_token"],
                refresh_token=response_data["refresh_token"],
                token_type=response_data.get("token_type", "bearer"),
                expires_in=expires_in,
                user=user,
                tenant=tenant,
                permissions=response_data.get("permissions", [])
            )
            
            await logger.ainfo(
                "User authenticated successfully",
                user_id=user.id,
                tenant_id=user.tenant_id,
                platform=data.get("platform", "unknown")
            )
            
            return auth_response
            
        except Exception as e:
            await logger.aerror(
                "Authentication failed",
                email=data.get("email", "unknown"),
                platform=data.get("platform", "unknown"),
                error=str(e)
            )
            raise
    
    async def logout(self) -> bool:
        """Logout user and invalidate tokens"""
        try:
            await self._make_request("POST", "/auth/sso/logout")
            
            # Clear stored tokens
            self._access_token = None
            self._refresh_token = None
            self._token_expires_at = None
            
            await logger.ainfo("User logged out successfully")
            return True
            
        except Exception as e:
            await logger.aerror("Logout failed", error=str(e))
            # Clear tokens even if logout failed
            self._access_token = None
            self._refresh_token = None
            self._token_expires_at = None
            return False
    
    async def get_current_user(self) -> Dict[str, Any]:
        """Get current user information"""
        return await self._make_request("GET", "/auth/me")
    
    async def authorize_platform(self, platform: str) -> Dict[str, Any]:
        """Check platform authorization for current user"""
        return await self._make_request("GET", f"/auth/authorize/{platform}")
    
    async def refresh_token(self) -> bool:
        """Refresh access token using refresh token"""
        try:
            if not self._refresh_token:
                raise AuthError("No refresh token available")
            
            data = {"refresh_token": self._refresh_token}
            response_data = await self._make_request(
                "POST", 
                "/auth/token/refresh", 
                data=data,
                include_auth=False
            )
            
            # Update tokens
            self._access_token = response_data["access_token"]
            expires_in = response_data.get("expires_in", 1800)
            self._token_expires_at = datetime.now(timezone.utc).timestamp() + expires_in
            
            await logger.ainfo("Token refreshed successfully")
            return True
            
        except Exception as e:
            await logger.aerror("Token refresh failed", error=str(e))
            # Clear tokens on refresh failure
            self._access_token = None
            self._refresh_token = None
            self._token_expires_at = None
            raise
    
    async def is_token_valid(self) -> bool:
        """Check if current access token is valid and not expired"""
        if not self._access_token or not self._token_expires_at:
            return False
        
        # Check if token expires in the next 5 minutes
        expires_buffer = 300  # 5 minutes
        return datetime.now(timezone.utc).timestamp() < (self._token_expires_at - expires_buffer)
    
    async def ensure_authenticated(self) -> bool:
        """Ensure we have a valid access token, refresh if necessary"""
        if await self.is_token_valid():
            return True
        
        if self._refresh_token:
            try:
                return await self.refresh_token()
            except Exception:
                return False
        
        return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check auth service health"""
        return await self._make_request("GET", "/health", include_auth=False)
    
    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register new user"""
        return await self._make_request(
            "POST", 
            "/auth/register", 
            data=user_data,
            include_auth=False
        )
    
    async def request_password_reset(self, email: str) -> Dict[str, Any]:
        """Request password reset for email"""
        return await self._make_request(
            "POST", 
            "/auth/forgot-password", 
            data={"email": email},
            include_auth=False
        )
    
    async def reset_password(self, token: str, password: str) -> Dict[str, Any]:
        """Reset password using reset token"""
        return await self._make_request(
            "POST", 
            "/auth/reset-password", 
            data={"token": token, "password": password},
            include_auth=False
        )
    
    async def verify_email(self, token: str) -> Dict[str, Any]:
        """Verify email address using verification token"""
        return await self._make_request(
            "POST", 
            "/auth/verify", 
            data={"token": token},
            include_auth=False
        )


# Utility functions for easy integration
async def quick_auth(
    email: str,
    password: str,
    platform: str = "bizosaas",
    base_url: str = "http://localhost:8007"
) -> AuthResponse:
    """Quick authentication helper"""
    async with AuthClient(base_url=base_url) as client:
        login_request = LoginRequest(
            email=email,
            password=password,
            platform=platform
        )
        return await client.login(login_request)


async def verify_platform_access(
    access_token: str,
    platform: str,
    base_url: str = "http://localhost:8007"
) -> bool:
    """Verify if token has access to platform"""
    try:
        async with AuthClient(base_url=base_url) as client:
            client._access_token = access_token
            result = await client.authorize_platform(platform)
            return result.get("authorized", False)
    except Exception:
        return False


# Rate-limited session manager for high-volume applications
class SessionManager:
    """Manage multiple authentication sessions with rate limiting"""
    
    def __init__(self, max_concurrent_sessions: int = 10):
        self.max_concurrent_sessions = max_concurrent_sessions
        self.sessions: Dict[str, AuthClient] = {}
        self.semaphore = asyncio.Semaphore(max_concurrent_sessions)
    
    async def create_session(
        self, 
        session_id: str, 
        base_url: str = "http://localhost:8007"
    ) -> AuthClient:
        """Create a new authentication session"""
        async with self.semaphore:
            if session_id in self.sessions:
                await self.sessions[session_id].close()
            
            client = AuthClient(base_url=base_url)
            self.sessions[session_id] = client
            return client
    
    async def get_session(self, session_id: str) -> Optional[AuthClient]:
        """Get existing session"""
        return self.sessions.get(session_id)
    
    async def remove_session(self, session_id: str):
        """Remove and close session"""
        if session_id in self.sessions:
            await self.sessions[session_id].close()
            del self.sessions[session_id]
    
    async def close_all_sessions(self):
        """Close all sessions"""
        for client in self.sessions.values():
            await client.close()
        self.sessions.clear()


if __name__ == "__main__":
    # Example usage
    async def main():
        # Quick authentication
        try:
            auth_response = await quick_auth(
                email="test@example.com",
                password="password123",
                platform="bizosaas"
            )
            print(f"Authenticated as: {auth_response.user.email}")
            print(f"Tenant: {auth_response.tenant.name}")
            print(f"Permissions: {auth_response.permissions}")
            
        except AuthError as e:
            print(f"Authentication failed: {e}")
    
    asyncio.run(main())