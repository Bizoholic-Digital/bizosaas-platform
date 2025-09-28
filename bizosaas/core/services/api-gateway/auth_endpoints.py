"""
Authentication endpoints for API Gateway
Handles login, registration, and tenant context
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET_KEY", "your-super-secret-jwt-key-change-in-production-make-it-very-long-and-random")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Request/Response Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    organization_name: str
    subscription_tier: str = "tier_1"
    domain: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class TenantContextResponse(BaseModel):
    tenant_id: str
    organization_name: str
    subscription_tier: str
    domain: str
    is_active: bool

# In-memory storage for development (replace with database in production)
USERS_DB = {}
ORGANIZATIONS_DB = {}

# Password utilities
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

# JWT utilities
def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
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

# Initialize demo data
def init_demo_data():
    """Initialize demo users and organizations"""
    demo_orgs = [
        {
            "id": "demo-org-1",
            "name": "Demo Marketing Agency",
            "domain": "localhost:3000",
            "subscription_tier": "tier_2",
            "is_active": True
        },
        {
            "id": "coreldove",
            "name": "Coreldove",
            "domain": "coreldove.com",
            "subscription_tier": "tier_3",
            "is_active": True
        }
    ]
    
    demo_users = [
        {
            "id": "demo-user-1",
            "email": "admin@bizosaas.com",
            "password": hash_password("admin123"),
            "organization_id": "demo-org-1",
            "role": "admin",
            "is_active": True
        },
        {
            "id": "coreldove-user",
            "email": "admin@coreldove.com", 
            "password": hash_password("coreldove123"),
            "organization_id": "coreldove",
            "role": "admin",
            "is_active": True
        }
    ]
    
    # Store in memory
    for org in demo_orgs:
        ORGANIZATIONS_DB[org["id"]] = org
    
    for user in demo_users:
        USERS_DB[user["email"]] = user
    
    logger.info("Demo data initialized")

# Authentication endpoints
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Authenticate user and return access token"""
    try:
        # Find user
        user = USERS_DB.get(request.email.lower())
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(request.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is disabled"
            )
        
        # Get organization
        organization = ORGANIZATIONS_DB.get(user["organization_id"])
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Organization not found"
            )
        
        # Create token payload
        token_data = {
            "user_id": user["id"],
            "email": user["email"],
            "organization_id": user["organization_id"],
            "role": user["role"],
            "subscription_tier": organization["subscription_tier"]
        }
        
        # Create access token
        access_token = create_access_token(token_data)
        
        # Prepare user data for response (excluding password)
        user_data = {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "organization_id": user["organization_id"],
            "organization_name": organization["name"],
            "subscription_tier": organization["subscription_tier"]
        }
        
        logger.info(f"User {user['email']} logged in successfully")
        
        return TokenResponse(
            access_token=access_token,
            user=user_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.post("/register", response_model=Dict[str, str])
async def register(request: RegisterRequest):
    """Register new user and organization"""
    try:
        # Check if user already exists
        if request.email.lower() in USERS_DB:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Validate subscription tier
        valid_tiers = ["tier_1", "tier_2", "tier_3"]
        if request.subscription_tier not in valid_tiers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid subscription tier"
            )
        
        # Create organization
        org_id = str(uuid.uuid4())
        organization = {
            "id": org_id,
            "name": request.organization_name,
            "domain": request.domain or f"{org_id}.bizosaas.com",
            "subscription_tier": request.subscription_tier,
            "is_active": True,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Create user
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "email": request.email.lower(),
            "password": hash_password(request.password),
            "organization_id": org_id,
            "role": "admin",  # First user in organization is admin
            "is_active": True,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store in database (memory for now)
        ORGANIZATIONS_DB[org_id] = organization
        USERS_DB[request.email.lower()] = user
        
        logger.info(f"New user registered: {user['email']} for organization: {organization['name']}")
        
        return {"message": "Account created successfully", "organization_id": org_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/tenant-context", response_model=TenantContextResponse)
async def get_tenant_context(domain: str):
    """Get tenant context by domain"""
    try:
        # Find organization by domain
        organization = None
        for org_id, org_data in ORGANIZATIONS_DB.items():
            if org_data["domain"] == domain:
                organization = org_data
                break
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found for this domain"
            )
        
        return TenantContextResponse(
            tenant_id=organization["id"],
            organization_name=organization["name"],
            subscription_tier=organization["subscription_tier"],
            domain=organization["domain"],
            is_active=organization["is_active"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tenant context error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me")
async def get_current_user_info(request: Request):
    """Get current user information from token"""
    try:
        # Get token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        # Find user
        user = USERS_DB.get(payload["email"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Get organization
        organization = ORGANIZATIONS_DB.get(user["organization_id"])
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Organization not found"
            )
        
        # Return user info (excluding password)
        return {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "organization_id": user["organization_id"],
            "organization_name": organization["name"],
            "subscription_tier": organization["subscription_tier"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user info error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Organization management endpoints
@router.get("/organizations/current")
async def get_current_organization(request: Request):
    """Get current user's organization details"""
    try:
        # Get token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        # Find user
        user = USERS_DB.get(payload["email"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Get organization
        organization = ORGANIZATIONS_DB.get(user["organization_id"])
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Organization not found"
            )
        
        return {
            "id": organization["id"],
            "name": organization["name"],
            "domain": organization["domain"],
            "subscription_tier": organization["subscription_tier"],
            "is_active": organization["is_active"],
            "bizosaas_tenant_id": organization["id"],  # Using org ID as tenant ID for demo
            "settings": {}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current organization error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/organizations/{organization_id}/usage")
async def get_organization_usage(organization_id: str, request: Request):
    """Get organization usage statistics"""
    try:
        # Verify authentication
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header"
            )
        
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        
        # Verify user has access to this organization
        user = USERS_DB.get(payload["email"])
        if not user or user["organization_id"] != organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Mock usage data - in production would query actual databases
        return {
            "products": 45,  # Current products in Saleor
            "orders": 156,   # Orders this month
            "staff": 3,      # Staff users
            "storage": 2.4   # Storage used in GB
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get organization usage error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Health check for auth service
@router.get("/health")
async def auth_health():
    """Authentication service health check"""
    return {
        "status": "healthy",
        "service": "authentication",
        "timestamp": datetime.utcnow().isoformat(),
        "users_count": len(USERS_DB),
        "organizations_count": len(ORGANIZATIONS_DB)
    }

# Initialize demo data when module loads
init_demo_data()