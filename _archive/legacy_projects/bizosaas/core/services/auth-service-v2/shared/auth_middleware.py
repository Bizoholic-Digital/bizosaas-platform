"""
Authentication Middleware for BizOSaas Services
Provides automatic authentication and authorization for all microservices
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Callable
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
import httpx
from jose import JWTError, jwt

from .vault_client import VaultClient
from .logging_system import get_logger, LogLevel, LogCategory

class AuthenticationError(Exception):
    """Custom authentication error"""
    pass

class AuthorizationError(Exception):
    """Custom authorization error"""
    pass

class BizOSaaSAuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware for BizOSaas services
    Handles JWT validation, service authorization, and user context
    """
    
    def __init__(self, 
                 app,
                 auth_service_url: str = "http://localhost:8003",
                 service_name: str = "unknown-service",
                 required_role: Optional[str] = None,
                 public_paths: List[str] = None,
                 admin_paths: List[str] = None):
        super().__init__(app)
        self.auth_service_url = auth_service_url.rstrip('/')
        self.service_name = service_name
        self.required_role = required_role
        self.public_paths = public_paths or ['/health', '/docs', '/redoc', '/openapi.json']
        self.admin_paths = admin_paths or []
        
        # Initialize components
        self.vault_client = VaultClient()
        self.logger = get_logger()
        self.http_client = httpx.AsyncClient(timeout=10.0)
        
        # Get JWT secret from Vault
        auth_secrets = self.vault_client.get_secret("auth/secrets") or {}
        self.jwt_secret = auth_secrets.get("jwt_secret", "change-me-jwt-secret")
        self.algorithm = "HS256"

    async def dispatch(self, request: Request, call_next):
        """Main middleware dispatch"""
        try:
            # Check if path is public
            if self._is_public_path(request.url.path):
                return await call_next(request)
            
            # Extract and validate token
            token = await self._extract_token(request)
            if not token:
                return await self._unauthorized_response("Missing authentication token")
            
            # Validate token and get user context
            user_context = await self._validate_token(token)
            if not user_context:
                return await self._unauthorized_response("Invalid authentication token")
            
            # Check service authorization
            if not await self._check_service_authorization(user_context):
                return await self._forbidden_response("Access denied to this service")
            
            # Check role requirements
            if not self._check_role_requirements(request.url.path, user_context):
                return await self._forbidden_response("Insufficient permissions")
            
            # Add user context to request state
            request.state.user = user_context
            request.state.authenticated = True
            
            # Log successful authentication
            await self.logger.log(
                LogLevel.INFO,
                LogCategory.AUTHENTICATION,
                self.service_name,
                f"Authenticated request: {request.method} {request.url.path}",
                details={
                    "user_id": user_context.get("user_id"),
                    "tenant_id": user_context.get("tenant_id"),
                    "role": user_context.get("role")
                },
                user_id=user_context.get("user_id"),
                tenant_id=user_context.get("tenant_id")
            )
            
            # Continue with request
            response = await call_next(request)
            
            return response
            
        except AuthenticationError as e:
            await self.logger.log(
                LogLevel.WARNING,
                LogCategory.AUTHENTICATION,
                self.service_name,
                f"Authentication failed: {str(e)}",
                details={"path": request.url.path, "method": request.method}
            )
            return await self._unauthorized_response(str(e))
            
        except AuthorizationError as e:
            await self.logger.log(
                LogLevel.WARNING,
                LogCategory.SECURITY,
                self.service_name,
                f"Authorization failed: {str(e)}",
                details={"path": request.url.path, "method": request.method}
            )
            return await self._forbidden_response(str(e))
            
        except Exception as e:
            await self.logger.log(
                LogLevel.ERROR,
                LogCategory.SYSTEM,
                self.service_name,
                f"Authentication middleware error: {str(e)}",
                details={"path": request.url.path, "method": request.method},
                error=e
            )
            return await self._internal_error_response("Authentication system error")

    def _is_public_path(self, path: str) -> bool:
        """Check if the path is public and doesn't require authentication"""
        return any(path.startswith(public_path) for public_path in self.public_paths)

    async def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from request headers"""
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix
        
        # Check cookies
        token = request.cookies.get("bizosaas_auth")
        if token:
            return token
        
        # Check custom header
        token = request.headers.get("X-BizOSaas-Token")
        if token:
            return token
            
        return None

    async def _validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return user context"""
        try:
            # First, try to validate locally
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.algorithm])
            
            # Basic validation
            if payload.get("exp", 0) < datetime.utcnow().timestamp():
                raise AuthenticationError("Token expired")
            
            # If local validation passes, verify with auth service
            user_context = await self._verify_with_auth_service(token)
            return user_context
            
        except JWTError as e:
            await self.logger.log(
                LogLevel.WARNING,
                LogCategory.AUTHENTICATION,
                self.service_name,
                f"JWT validation failed: {str(e)}"
            )
            return None
        except Exception as e:
            await self.logger.log(
                LogLevel.ERROR,
                LogCategory.AUTHENTICATION,
                self.service_name,
                f"Token validation error: {str(e)}",
                error=e
            )
            return None

    async def _verify_with_auth_service(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify token with central auth service"""
        try:
            response = await self.http_client.get(
                f"{self.auth_service_url}/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Extract relevant context
                return {
                    "user_id": user_data["user"]["id"],
                    "email": user_data["user"]["email"],
                    "role": user_data["user"]["role"],
                    "tenant_id": user_data["user"]["tenant_id"],
                    "tenant_slug": user_data["tenant"]["slug"],
                    "tenant_name": user_data["tenant"]["name"],
                    "allowed_services": user_data["user"]["allowed_services"],
                    "allowed_platforms": user_data["tenant"]["allowed_platforms"],
                    "is_super_admin": user_data["permissions"]["is_super_admin"],
                    "token": token
                }
            
            return None
            
        except Exception as e:
            await self.logger.log(
                LogLevel.ERROR,
                LogCategory.AUTHENTICATION,
                self.service_name,
                f"Auth service verification failed: {str(e)}",
                error=e
            )
            return None

    async def _check_service_authorization(self, user_context: Dict[str, Any]) -> bool:
        """Check if user has access to this service"""
        try:
            response = await self.http_client.get(
                f"{self.auth_service_url}/auth/authorize/{self.service_name}",
                headers={"Authorization": f"Bearer {user_context['token']}"}
            )
            
            return response.status_code == 200
            
        except Exception as e:
            await self.logger.log(
                LogLevel.ERROR,
                LogCategory.AUTHENTICATION,
                self.service_name,
                f"Service authorization check failed: {str(e)}",
                error=e
            )
            return False

    def _check_role_requirements(self, path: str, user_context: Dict[str, Any]) -> bool:
        """Check role-based access requirements"""
        user_role = user_context.get("role")
        is_super_admin = user_context.get("is_super_admin", False)
        
        # Super admin has access to everything
        if is_super_admin:
            return True
        
        # Check admin paths
        if any(path.startswith(admin_path) for admin_path in self.admin_paths):
            return user_role in ["super_admin", "tenant_admin"]
        
        # Check service-specific role requirements
        if self.required_role:
            role_hierarchy = {
                "readonly": 0,
                "user": 1,
                "tenant_admin": 2,
                "super_admin": 3
            }
            
            required_level = role_hierarchy.get(self.required_role, 999)
            user_level = role_hierarchy.get(user_role, -1)
            
            return user_level >= required_level
        
        # Default: allow all authenticated users
        return True

    async def _unauthorized_response(self, message: str):
        """Return 401 Unauthorized response"""
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": message,
                "type": "authentication_error",
                "service": self.service_name
            },
            headers={"WWW-Authenticate": "Bearer"}
        )

    async def _forbidden_response(self, message: str):
        """Return 403 Forbidden response"""
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": message,
                "type": "authorization_error",
                "service": self.service_name
            }
        )

    async def _internal_error_response(self, message: str):
        """Return 500 Internal Server Error response"""
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": message,
                "type": "internal_error",
                "service": self.service_name
            }
        )

# Dependency for FastAPI routes
class AuthDependency:
    """FastAPI dependency for authentication"""
    
    def __init__(self, required_role: Optional[str] = None, required_service: Optional[str] = None):
        self.required_role = required_role
        self.required_service = required_service

    async def __call__(self, request: Request) -> Dict[str, Any]:
        """Get authenticated user from request state"""
        if not hasattr(request.state, "authenticated") or not request.state.authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        user_context = request.state.user
        
        # Check role requirement
        if self.required_role:
            user_role = user_context.get("role")
            is_super_admin = user_context.get("is_super_admin", False)
            
            if not is_super_admin and user_role != self.required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Requires {self.required_role} role"
                )
        
        # Check service requirement
        if self.required_service:
            allowed_services = user_context.get("allowed_services", [])
            allowed_platforms = user_context.get("allowed_platforms", [])
            is_super_admin = user_context.get("is_super_admin", False)
            
            if not is_super_admin and self.required_service not in allowed_services and self.required_service not in allowed_platforms:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied to {self.required_service} service"
                )
        
        return user_context

# Convenient dependency instances
authenticated_user = AuthDependency()
admin_user = AuthDependency(required_role="tenant_admin")
super_admin_user = AuthDependency(required_role="super_admin")

def require_service(service_name: str):
    """Create dependency that requires specific service access"""
    return AuthDependency(required_service=service_name)

# Utility functions for service integration
async def validate_service_token(token: str, service_name: str) -> Optional[Dict[str, Any]]:
    """Standalone function to validate token for a service"""
    auth_service_url = "http://localhost:8003"
    
    try:
        async with httpx.AsyncClient() as client:
            # Verify token
            response = await client.get(
                f"{auth_service_url}/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                return None
            
            user_data = response.json()
            
            # Check service authorization
            auth_response = await client.get(
                f"{auth_service_url}/auth/authorize/{service_name}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if auth_response.status_code != 200:
                return None
            
            return {
                "user_id": user_data["user"]["id"],
                "email": user_data["user"]["email"],
                "role": user_data["user"]["role"],
                "tenant_id": user_data["user"]["tenant_id"],
                "tenant_slug": user_data["tenant"]["slug"],
                "is_super_admin": user_data["permissions"]["is_super_admin"]
            }
            
    except Exception:
        return None

def create_auth_headers(token: str) -> Dict[str, str]:
    """Create authentication headers for service-to-service calls"""
    return {
        "Authorization": f"Bearer {token}",
        "X-BizOSaas-Service": "internal"
    }