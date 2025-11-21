#!/usr/bin/env python3
"""
BizOSaaS Platform - Authentication Service v2
Port: 8007
Purpose: Unified authentication hub with JWT management and role-based access control
"""

import os
import uuid
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Depends, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import jwt
import uvicorn
from passlib.context import CryptContext
import redis
import asyncpg
import asyncio
from contextlib import asynccontextmanager

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "auth-service-secret-key-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour (security best practice)
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:securepassword@localhost:5432/bizosaas")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Global connections
db_pool = None
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global db_pool, redis_client
    
    # Startup
    try:
        # Initialize database connection pool
        db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=5, max_size=20)
        print("✅ Database connection pool created")
        
        # Initialize Redis connection
        redis_client = redis.from_url(REDIS_URL)
        redis_client.ping()
        print("✅ Redis connection established")
        
        # Create tables if not exist
        await create_tables()
        print("✅ Database tables verified")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    if db_pool:
        await db_pool.close()
    if redis_client:
        redis_client.close()

# FastAPI app
app = FastAPI(
    title="BizOSaaS Authentication Service v2",
    description="Unified authentication hub with JWT management and RBAC",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "client"
    tenant_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class StandardResponse(BaseModel):
    """Standardized API response format"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

class TokenData(BaseModel):
    """Token data returned in standardized response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class TokenResponse(BaseModel):
    """Legacy token response for backward compatibility"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    tenant_id: Optional[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]

# Database setup
async def create_tables():
    """Create necessary tables if they don't exist"""
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'client',
                tenant_id UUID,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            );
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS refresh_tokens (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID REFERENCES users(id) ON DELETE CASCADE,
                token_hash VARCHAR(255) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP,
                is_revoked BOOLEAN DEFAULT false
            );
        """)
        
        await conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
            CREATE INDEX IF NOT EXISTS idx_users_tenant_id ON users(tenant_id);
            CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id);
        """)

# Utility functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token() -> str:
    """Create refresh token"""
    return str(uuid.uuid4())

async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
        return dict(row) if row else None

async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        return dict(row) if row else None

async def create_user(user_data: UserCreate) -> Dict[str, Any]:
    """Create new user"""
    password_hash = hash_password(user_data.password)
    
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO users (email, password_hash, full_name, role, tenant_id)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        """, user_data.email, password_hash, user_data.full_name, 
            user_data.role, user_data.tenant_id)
        
        return dict(row)

async def store_refresh_token(user_id: str, refresh_token: str) -> None:
    """Store refresh token in database"""
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO refresh_tokens (user_id, token_hash, expires_at)
            VALUES ($1, $2, $3)
        """, user_id, token_hash, expires_at)

async def verify_refresh_token(refresh_token: str) -> Optional[str]:
    """Verify refresh token and return user_id"""
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
    
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT user_id FROM refresh_tokens 
            WHERE token_hash = $1 AND expires_at > CURRENT_TIMESTAMP AND is_revoked = false
        """, token_hash)
        
        return str(row['user_id']) if row else None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        async with db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        
        # Test Redis connection
        redis_client.ping()
        
        return {
            "status": "healthy",
            "service": "auth-service-v2",
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "port": 8007,
            "database": "connected",
            "redis": "connected"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@app.post("/auth/register")
async def register(user_data: UserCreate, response: Response):
    """Register new user with HttpOnly cookie for refresh token"""
    # Check if user already exists
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = await create_user(user_data)

    # Create tokens
    access_token = create_access_token(data={"sub": str(user["id"])})
    refresh_token = create_refresh_token()
    await store_refresh_token(str(user["id"]), refresh_token)

    # Cache user session
    session_key = f"session:{user['id']}"
    redis_client.setex(session_key, 3600, json.dumps({
        "user_id": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
        "tenant_id": str(user["tenant_id"]) if user["tenant_id"] else None
    }))

    # Set HttpOnly cookie for refresh token
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/auth"
    )

    # Return standardized response
    return StandardResponse(
        success=True,
        data=TokenData(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": str(user["id"]),
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "tenant_id": str(user["tenant_id"]) if user["tenant_id"] else None
            }
        ).dict()
    )

@app.post("/auth/login")
async def login(login_data: UserLogin, response: Response):
    """User login with HttpOnly cookie for refresh token"""
    # Verify user credentials
    user = await get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user["is_active"]:
        raise HTTPException(status_code=401, detail="Account is deactivated")

    # Update last login
    async with db_pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1",
            user["id"]
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user["id"])})
    refresh_token = create_refresh_token()
    await store_refresh_token(str(user["id"]), refresh_token)

    # Cache user session
    session_key = f"session:{user['id']}"
    redis_client.setex(session_key, 3600, json.dumps({
        "user_id": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
        "tenant_id": str(user["tenant_id"]) if user["tenant_id"] else None
    }))

    # Set HttpOnly cookie for refresh token (SECURITY: XSS-proof)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # Cannot be accessed by JavaScript
        secure=True,  # HTTPS only in production
        samesite="lax",  # CSRF protection
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 30 days
        path="/api/auth"  # Only sent to auth endpoints
    )

    # Return standardized response with access token (NOT refresh token)
    return StandardResponse(
        success=True,
        data=TokenData(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": str(user["id"]),
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "tenant_id": str(user["tenant_id"]) if user["tenant_id"] else None
            }
        ).dict()
    )

@app.post("/auth/refresh")
async def refresh_token_endpoint(request: Request, response: Response):
    """Refresh access token with token rotation (security best practice)"""
    # Get refresh token from HttpOnly cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    # Validate refresh token and get token record
    token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

    async with db_pool.acquire() as conn:
        token_row = await conn.fetchrow("""
            SELECT * FROM refresh_tokens
            WHERE token_hash = $1 AND expires_at > CURRENT_TIMESTAMP AND is_revoked = false
        """, token_hash)

        if not token_row:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        # Check for token reuse (security)
        if token_row['last_used_at'] is not None:
            time_since_last_use = datetime.utcnow() - token_row['last_used_at']
            if time_since_last_use.total_seconds() < 5:
                # Token reused within 5 seconds - possible attack
                # Revoke all tokens for user
                await conn.execute("""
                    UPDATE refresh_tokens SET is_revoked = true WHERE user_id = $1
                """, token_row['user_id'])
                raise HTTPException(status_code=401, detail="Token reuse detected - all sessions revoked")

        # Mark current token as used
        await conn.execute("""
            UPDATE refresh_tokens SET last_used_at = CURRENT_TIMESTAMP WHERE id = $1
        """, token_row['id'])

        # Get user
        user = await get_user_by_id(str(token_row['user_id']))
        if not user or not user["is_active"]:
            raise HTTPException(status_code=401, detail="User not found or inactive")

        # Revoke old refresh token (rotation)
        await conn.execute("""
            UPDATE refresh_tokens SET is_revoked = true WHERE id = $1
        """, token_row['id'])

    # Create new tokens
    access_token = create_access_token(data={"sub": str(user["id"])})
    new_refresh_token = create_refresh_token()
    await store_refresh_token(str(user["id"]), new_refresh_token)

    # Set new refresh token cookie (rotation)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/auth"
    )

    # Return standardized response with new access token
    return StandardResponse(
        success=True,
        data=TokenData(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": str(user["id"]),
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "tenant_id": str(user["tenant_id"]) if user["tenant_id"] else None
            }
        ).dict()
    )

@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=str(current_user["id"]),
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        tenant_id=str(current_user["tenant_id"]) if current_user["tenant_id"] else None,
        is_active=current_user["is_active"],
        created_at=current_user["created_at"],
        last_login=current_user["last_login"]
    )

@app.post("/auth/logout")
async def logout(response: Response, current_user: Dict = Depends(get_current_user)):
    """User logout - revoke tokens and clear cookies"""
    # Revoke all refresh tokens for user
    async with db_pool.acquire() as conn:
        await conn.execute(
            "UPDATE refresh_tokens SET is_revoked = true WHERE user_id = $1",
            current_user["id"]
        )

    # Remove session cache
    session_key = f"session:{current_user['id']}"
    redis_client.delete(session_key)

    # Clear refresh token cookie
    response.delete_cookie(key="refresh_token", path="/api/auth")

    return StandardResponse(
        success=True,
        message="Logged out successfully"
    )

@app.get("/auth/validate")
async def validate_token(current_user: Dict = Depends(get_current_user)):
    """Validate token and return user info"""
    return {
        "valid": True,
        "user": {
            "id": str(current_user["id"]),
            "email": current_user["email"],
            "role": current_user["role"],
            "tenant_id": str(current_user["tenant_id"]) if current_user["tenant_id"] else None
        }
    }

# Role-based access control endpoints
@app.get("/auth/permissions/{platform}")
async def get_platform_permissions(platform: str, current_user: Dict = Depends(get_current_user)):
    """Get user permissions for specific platform"""
    role = current_user["role"]
    
    # Platform access matrix from PRD
    permissions = {
        "super_admin": {
            "bizosaas_admin": True,  # Port 3001
            "sql_admin": True,       # Port 5000  
            "bizoholic": True,       # Port 3000
            "coreldove": True,       # Port 3002
            "ai_chat": True          # Port 3003
        },
        "tenant_admin": {
            "bizosaas_admin": True,  # Port 3001
            "bizoholic": True,       # Port 3000
            "coreldove": True,       # Port 3002
            "ai_chat": True,         # Port 3003
            "sql_admin": False       # Port 5000
        },
        "manager": {
            "bizoholic": True,       # Port 3000
            "coreldove": True,       # Port 3002
            "ai_chat": True,         # Port 3003
            "bizosaas_admin": False, # Port 3001
            "sql_admin": False       # Port 5000
        },
        "client": {
            "ai_chat": True,         # Port 3003
            "client_portal": True,   # Limited access
            "bizoholic": False,      # Port 3000
            "coreldove": False,      # Port 3002
            "bizosaas_admin": False, # Port 3001
            "sql_admin": False       # Port 5000
        }
    }
    
    user_permissions = permissions.get(role, permissions["client"])
    platform_access = user_permissions.get(platform, False)
    
    return {
        "platform": platform,
        "user_role": role,
        "has_access": platform_access,
        "permissions": user_permissions
    }

if __name__ == "__main__":
    print("🚀 Starting Authentication Service v2 on port 8007...")
    print("🔐 Unified authentication hub with JWT management and RBAC")
    print("🔗 Integrates with BizOSaaS Platform ecosystem")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8007,
        reload=True,
        log_level="info"
    )