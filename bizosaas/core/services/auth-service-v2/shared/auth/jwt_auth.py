"""
Shared JWT authentication and authorization system for BizoholicSaaS microservices
Provides centralized authentication, RBAC, and multi-tenant security
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import redis.asyncio as redis
from enum import Enum

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()

class UserRole(Enum):
    """User roles with hierarchical permissions"""
    SUPER_ADMIN = "super_admin"      # Platform admin across all tenants
    TENANT_ADMIN = "tenant_admin"    # Full admin within tenant
    MANAGER = "manager"              # Campaign and user management
    USER = "user"                    # Standard user operations
    VIEWER = "viewer"                # Read-only access

class Permission(Enum):
    """Granular permissions for RBAC"""
    # User Management
    USER_CREATE = "user.create"
    USER_READ = "user.read"
    USER_UPDATE = "user.update"
    USER_DELETE = "user.delete"
    
    # Campaign Management
    CAMPAIGN_CREATE = "campaign.create"
    CAMPAIGN_READ = "campaign.read"
    CAMPAIGN_UPDATE = "campaign.update"
    CAMPAIGN_DELETE = "campaign.delete"
    CAMPAIGN_EXECUTE = "campaign.execute"
    
    # Analytics
    ANALYTICS_READ = "analytics.read"
    ANALYTICS_CREATE = "analytics.create"
    REPORT_GENERATE = "report.generate"
    DASHBOARD_MANAGE = "dashboard.manage"
    
    # Integration Management
    INTEGRATION_CREATE = "integration.create"
    INTEGRATION_READ = "integration.read"
    INTEGRATION_UPDATE = "integration.update"
    INTEGRATION_DELETE = "integration.delete"
    
    # AI Agents
    AGENT_EXECUTE = "agent.execute"
    AGENT_CONFIGURE = "agent.configure"
    AGENT_MONITOR = "agent.monitor"
    
    # Admin Functions
    TENANT_MANAGE = "tenant.manage"
    BILLING_MANAGE = "billing.manage"
    SYSTEM_MONITOR = "system.monitor"

# Role-Permission Mapping
ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: [p for p in Permission],  # All permissions
    
    UserRole.TENANT_ADMIN: [
        Permission.USER_CREATE, Permission.USER_READ, Permission.USER_UPDATE, Permission.USER_DELETE,
        Permission.CAMPAIGN_CREATE, Permission.CAMPAIGN_READ, Permission.CAMPAIGN_UPDATE, 
        Permission.CAMPAIGN_DELETE, Permission.CAMPAIGN_EXECUTE,
        Permission.ANALYTICS_READ, Permission.ANALYTICS_CREATE, Permission.REPORT_GENERATE,
        Permission.DASHBOARD_MANAGE,
        Permission.INTEGRATION_CREATE, Permission.INTEGRATION_READ, Permission.INTEGRATION_UPDATE,
        Permission.INTEGRATION_DELETE,
        Permission.AGENT_EXECUTE, Permission.AGENT_CONFIGURE, Permission.AGENT_MONITOR,
        Permission.BILLING_MANAGE
    ],
    
    UserRole.MANAGER: [
        Permission.USER_READ, Permission.USER_UPDATE,
        Permission.CAMPAIGN_CREATE, Permission.CAMPAIGN_READ, Permission.CAMPAIGN_UPDATE,
        Permission.CAMPAIGN_EXECUTE,
        Permission.ANALYTICS_READ, Permission.ANALYTICS_CREATE, Permission.REPORT_GENERATE,
        Permission.DASHBOARD_MANAGE,
        Permission.INTEGRATION_READ, Permission.INTEGRATION_UPDATE,
        Permission.AGENT_EXECUTE, Permission.AGENT_MONITOR
    ],
    
    UserRole.USER: [
        Permission.USER_READ,
        Permission.CAMPAIGN_READ, Permission.CAMPAIGN_UPDATE,
        Permission.ANALYTICS_READ, Permission.REPORT_GENERATE,
        Permission.INTEGRATION_READ,
        Permission.AGENT_EXECUTE
    ],
    
    UserRole.VIEWER: [
        Permission.USER_READ,
        Permission.CAMPAIGN_READ,
        Permission.ANALYTICS_READ,
        Permission.INTEGRATION_READ
    ]
}

class TokenData(BaseModel):
    """JWT token payload structure"""
    user_id: str
    tenant_id: str
    email: str
    role: UserRole
    permissions: List[Permission]
    exp: int
    iat: int
    jti: str  # JWT ID for token tracking

class UserContext(BaseModel):
    """Current user context for requests"""
    user_id: str
    tenant_id: str
    email: str
    role: UserRole
    permissions: List[Permission]
    is_authenticated: bool = True

class JWTManager:
    """JWT token management and validation"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client
    
    def create_access_token(
        self, 
        user_id: str, 
        tenant_id: str, 
        email: str, 
        role: UserRole,
        permissions: Optional[List[Permission]] = None
    ) -> str:
        """Create JWT access token"""
        
        if permissions is None:
            permissions = ROLE_PERMISSIONS.get(role, [])
        
        now = datetime.utcnow()
        expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        payload = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "email": email,
            "role": role.value,
            "permissions": [p.value for p in permissions],
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "jti": f"{user_id}:{int(now.timestamp())}"
        }
        
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    def create_refresh_token(self, user_id: str, tenant_id: str) -> str:
        """Create JWT refresh token"""
        now = datetime.utcnow()
        expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        payload = {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "type": "refresh",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "jti": f"refresh:{user_id}:{int(now.timestamp())}"
        }
        
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> TokenData:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            
            # Check if token is blacklisted (if Redis is available)
            if self.redis_client:
                is_blacklisted = asyncio.create_task(
                    self.redis_client.exists(f"blacklisted_token:{payload.get('jti')}")
                )
                if is_blacklisted:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token has been revoked"
                    )
            
            return TokenData(
                user_id=payload["user_id"],
                tenant_id=payload["tenant_id"],
                email=payload["email"],
                role=UserRole(payload["role"]),
                permissions=[Permission(p) for p in payload["permissions"]],
                exp=payload["exp"],
                iat=payload["iat"],
                jti=payload["jti"]
            )
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def revoke_token(self, token_data: TokenData):
        """Revoke a JWT token by adding to blacklist"""
        if self.redis_client:
            # Calculate remaining TTL for the token
            exp_timestamp = token_data.exp
            current_timestamp = int(datetime.utcnow().timestamp())
            ttl = max(0, exp_timestamp - current_timestamp)
            
            if ttl > 0:
                await self.redis_client.setex(
                    f"blacklisted_token:{token_data.jti}",
                    ttl,
                    "revoked"
                )

class PasswordManager:
    """Password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# Global JWT manager instance
jwt_manager = JWTManager()

def set_redis_client(redis_client: redis.Redis):
    """Set Redis client for JWT manager"""
    jwt_manager.redis_client = redis_client

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserContext:
    """Get current authenticated user from JWT token"""
    
    try:
        token = credentials.credentials
        token_data = jwt_manager.verify_token(token)
        
        return UserContext(
            user_id=token_data.user_id,
            tenant_id=token_data.tenant_id,
            email=token_data.email,
            role=token_data.role,
            permissions=token_data.permissions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Optional authentication (allows both authenticated and anonymous)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[UserContext]:
    """Get current user if authenticated, None if not"""
    
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

# Permission checking functions
def require_permission(permission: Permission):
    """Dependency to require specific permission"""
    def permission_checker(current_user: UserContext = Depends(get_current_user)):
        if permission not in current_user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {permission.value}"
            )
        return current_user
    return permission_checker

def require_role(minimum_role: UserRole):
    """Dependency to require minimum role level"""
    role_hierarchy = [
        UserRole.VIEWER,
        UserRole.USER,
        UserRole.MANAGER,
        UserRole.TENANT_ADMIN,
        UserRole.SUPER_ADMIN
    ]
    
    def role_checker(current_user: UserContext = Depends(get_current_user)):
        user_role_level = role_hierarchy.index(current_user.role)
        required_role_level = role_hierarchy.index(minimum_role)
        
        if user_role_level < required_role_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient role. Required: {minimum_role.value}"
            )
        return current_user
    return role_checker

def require_tenant_access(tenant_id: str):
    """Dependency to require access to specific tenant"""
    def tenant_checker(current_user: UserContext = Depends(get_current_user)):
        if current_user.role != UserRole.SUPER_ADMIN and current_user.tenant_id != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this tenant"
            )
        return current_user
    return tenant_checker

# Convenience dependencies for common permission patterns
def require_campaign_read():
    return require_permission(Permission.CAMPAIGN_READ)

def require_campaign_write():
    return require_permission(Permission.CAMPAIGN_CREATE)

def require_campaign_execute():
    return require_permission(Permission.CAMPAIGN_EXECUTE)

def require_analytics_access():
    return require_permission(Permission.ANALYTICS_READ)

def require_integration_manage():
    return require_permission(Permission.INTEGRATION_CREATE)

def require_agent_execute():
    return require_permission(Permission.AGENT_EXECUTE)

def require_admin():
    return require_role(UserRole.TENANT_ADMIN)

def require_manager():
    return require_role(UserRole.MANAGER)

# Service-to-service authentication
class ServiceAuthToken:
    """Service-to-service authentication token"""
    
    SERVICE_SECRET = os.getenv("SERVICE_SECRET", "service-to-service-secret-key")
    
    @classmethod
    def create_service_token(cls, service_name: str, target_service: str) -> str:
        """Create service-to-service authentication token"""
        now = datetime.utcnow()
        expire = now + timedelta(minutes=5)  # Short-lived service tokens
        
        payload = {
            "service_name": service_name,
            "target_service": target_service,
            "type": "service",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp())
        }
        
        return jwt.encode(payload, cls.SERVICE_SECRET, algorithm=JWT_ALGORITHM)
    
    @classmethod
    def verify_service_token(cls, token: str, expected_service: str) -> bool:
        """Verify service-to-service token"""
        try:
            payload = jwt.decode(token, cls.SERVICE_SECRET, algorithms=[JWT_ALGORITHM])
            return (
                payload.get("type") == "service" and 
                payload.get("target_service") == expected_service
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False

# Middleware for service authentication
async def verify_service_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    expected_service: str = "api-gateway"
) -> bool:
    """Verify service-to-service authentication"""
    
    if not ServiceAuthToken.verify_service_token(credentials.credentials, expected_service):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service authentication"
        )
    return True