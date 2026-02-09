# Auth Service - Backend Service (DDD)

## Service Identity
- **Name**: Authentication Service v2
- **Type**: Backend - Authentication & Authorization
- **Container**: `bizosaas-auth-staging`
- **Image**: `bizosaas/auth-service-v2:latest`
- **Port**: `8007:8007`
- **Status**: ✅ Running (15+ hours uptime)

## Purpose
Multi-tenant authentication and authorization using FastAPI-Users v12 with JWT tokens, role-based access control (RBAC), and unified SSO across all BizOSaaS platforms.

## Domain-Driven Design Architecture

### Bounded Context: Identity & Access Management

```
Auth Bounded Context
├── Domain Layer
│   ├── Aggregates: User, Tenant, Role
│   ├── Entities: Session, RefreshToken, Permission
│   ├── Value Objects: Email, Password, JWTToken
│   ├── Domain Events: UserRegistered, UserLoggedIn, RoleAssigned
│   └── Domain Services: PasswordHasher, TokenGenerator, PermissionChecker
├── Application Layer
│   ├── Commands: RegisterUserCommand, LoginCommand, AssignRoleCommand
│   ├── Queries: GetUserQuery, ValidateTokenQuery
│   └── Handlers: AuthenticationHandler, AuthorizationHandler
├── Infrastructure Layer
│   ├── FastAPI-Users Integration
│   ├── PostgreSQL User Store
│   ├── Redis Session Store
│   └── JWT Token Management
└── API Layer
    ├── /auth/register
    ├── /auth/login
    ├── /auth/logout
    ├── /auth/refresh
    └── /auth/verify
```

### Core Aggregates

#### User Aggregate
```python
class UserRole(Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    MANAGER = "manager"
    CLIENT = "client"

class User:
    """User aggregate with multi-tenant support"""
    def __init__(self, id: UUID, email: Email, tenant_id: UUID):
        self.id = id
        self.email = email
        self.tenant_id = tenant_id
        self.password_hash: str = ""
        self.roles: List[UserRole] = []
        self.is_active = True
        self.is_verified = False
        self.created_at = datetime.utcnow()
        self._domain_events = []

    def assign_role(self, role: UserRole):
        if role not in self.roles:
            self.roles.append(role)
            self._add_domain_event(RoleAssignedEvent(
                user_id=self.id,
                role=role,
                tenant_id=self.tenant_id
            ))

    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        role_permissions = {
            UserRole.SUPER_ADMIN: ["*"],  # All permissions
            UserRole.TENANT_ADMIN: ["tenant.*", "users.*"],
            UserRole.MANAGER: ["campaigns.*", "leads.*"],
            UserRole.CLIENT: ["campaigns.view", "leads.view"]
        }
        
        for role in self.roles:
            if "*" in role_permissions.get(role, []):
                return True
            if permission in role_permissions.get(role, []):
                return True
        
        return False
```

## API Endpoints

### User Registration
```python
@router.post("/auth/register")
async def register(request: RegisterRequest):
    """
    Register new user
    
    Body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "tenant_id": "uuid",
        "role": "client"
    }
    """
    # Validate email uniqueness
    # Hash password
    # Create user
    # Publish UserRegisteredEvent
    # Send verification email
    
    return {
        "user_id": str(user.id),
        "email": user.email,
        "status": "pending_verification"
    }
```

### User Login
```python
@router.post("/auth/login")
async def login(request: LoginRequest):
    """
    User login with JWT token generation
    
    Body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    
    Returns:
    {
        "access_token": "eyJ...",
        "refresh_token": "eyJ...",
        "token_type": "bearer",
        "expires_in": 3600
    }
    """
    # Validate credentials
    # Generate JWT access token (1 hour)
    # Generate refresh token (7 days)
    # Store session in Redis
    # Publish UserLoggedInEvent
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600
    }
```

### Token Refresh
```python
@router.post("/auth/refresh")
async def refresh_token(request: RefreshRequest):
    """Refresh access token using refresh token"""
    # Validate refresh token
    # Check token not blacklisted
    # Generate new access token
    # Return new tokens
```

### Unified SSO
```python
@router.get("/auth/sso/platforms")
async def get_user_platforms(
    user_id: UUID = Depends(get_current_user)
):
    """
    Get platforms user has access to
    
    Returns:
    {
        "platforms": [
            {
                "name": "Bizoholic Marketing",
                "url": "http://stg.bizoholic.com",
                "port": 3008,
                "accessible": true
            },
            {
                "name": "CorelDove E-commerce",
                "url": "http://stg.coreldove.com",
                "port": 3007,
                "accessible": true
            },
            {
                "name": "Client Portal",
                "port": 3006,
                "accessible": true
            },
            {
                "name": "BizOSaaS Admin",
                "port": 3009,
                "accessible": false  # Not super_admin
            }
        ]
    }
    """
```

## Multi-Tenancy

### Tenant Context Middleware
```python
@app.middleware("http")
async def tenant_context_middleware(request: Request, call_next):
    """Extract and validate tenant context"""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if token:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        request.state.tenant_id = UUID(payload["tenant_id"])
        request.state.user_id = UUID(payload["sub"])
        request.state.roles = payload.get("roles", [])
    
    response = await call_next(request)
    return response
```

## Configuration

```bash
# Auth Service
AUTH_SERVICE_HOST=0.0.0.0
AUTH_SERVICE_PORT=8007

# JWT Configuration
JWT_SECRET_KEY=vault:secret/encryption/jwt#signing_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://postgres:password@bizosaas-postgres-staging:5432/bizosaas_platform

# Redis (sessions)
REDIS_URL=redis://bizosaas-redis-staging:6379/3

# Email (verification)
SMTP_HOST=smtp.resend.com
SMTP_PORT=587
SMTP_USER=resend
SMTP_PASSWORD=vault:secret/apis/resend#api_key
```

## Deployment Checklist
- [x] Auth service container deployed
- [x] FastAPI-Users v12 configured
- [x] JWT token generation working
- [x] Redis session storage active
- [x] Multi-tenant isolation enforced
- [x] SSO across platforms enabled

---
**Status**: ✅ Production-Ready
**Last Updated**: October 15, 2025
