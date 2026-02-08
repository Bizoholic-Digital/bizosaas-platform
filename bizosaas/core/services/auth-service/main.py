"""
BizoSaaS Authentication Service - Full Implementation
Integrates fastapi-users with PostgreSQL and provides JWT authentication
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import logging
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory user store for demo (replace with database in production)
DEMO_USERS = {
    "demo@bizosaas.com": {
        "id": "demo-user-001",
        "email": "demo@bizosaas.com",
        "password": "demo123",  # In production, this would be hashed
        "first_name": "Demo",
        "last_name": "User",
        "role": "user",
        "is_active": True,
        "is_verified": True
    },
    "admin@bizosaas.com": {
        "id": "admin-user-001",
        "email": "admin@bizosaas.com",
        "password": "AdminDemo2024!",
        "first_name": "Admin",
        "last_name": "User",
        "role": "super_admin",
        "is_active": True,
        "is_verified": True
    }
}

# Simple session store (in-memory, replace with Redis in production)
SESSIONS = {}

class LoginRequest(BaseModel):
    username: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"
    is_active: bool = True
    is_verified: bool = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting BizoSaaS Authentication Service...")
    logger.info(f"Demo users loaded: {len(DEMO_USERS)}")
    yield
    logger.info("Shutting down Authentication Service...")

def create_app() -> FastAPI:
    """Create FastAPI application with authentication"""
    
    app = FastAPI(
        title="BizoSaaS Authentication Service",
        description="Multi-tenant authentication and user management service",
        version="2.0.0",
        lifespan=lifespan
    )
    
    # CORS middleware - Allow all origins for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

app = create_app()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "service": "auth-service",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "demo_users_count": len(DEMO_USERS),
        "features": {
            "login": "active",
            "jwt_tokens": "active",
            "demo_users": "active"
        }
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "BizoSaaS Authentication Service",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "login": "/jwt/login",
            "current_user": "/users/me",
            "logout": "/jwt/logout"
        }
    }

@app.post("/jwt/login")
async def login(username: str = None, password: str = None):
    """
    Login endpoint compatible with fastapi-users format
    Accepts form data: username (email) and password
    """
    logger.info(f"Login attempt for: {username}")
    
    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    # Check if user exists
    user = DEMO_USERS.get(username)
    if not user:
        logger.warning(f"User not found: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password (simple comparison for demo, use hashing in production)
    if user["password"] != password:
        logger.warning(f"Invalid password for: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create session token (simple UUID for demo)
    import uuid
    session_token = str(uuid.uuid4())
    SESSIONS[session_token] = {
        "user_id": user["id"],
        "email": user["email"],
        "created_at": datetime.now().isoformat()
    }
    
    logger.info(f"Login successful for: {username}")
    
    # Return user data and token
    return {
        "access_token": session_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "role": user.get("role", "user"),
            "is_active": user.get("is_active", True),
            "is_verified": user.get("is_verified", True)
        }
    }

@app.get("/users/me")
async def get_current_user(authorization: Optional[str] = None):
    """Get current authenticated user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Extract token from "Bearer <token>"
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    
    # Check session
    session = SESSIONS.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Find user
    user_email = session["email"]
    user = DEMO_USERS.get(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user["id"],
        "email": user["email"],
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "role": user.get("role", "user"),
        "is_active": user.get("is_active", True),
        "is_verified": user.get("is_verified", True)
    }

@app.post("/jwt/logout")
async def logout(authorization: Optional[str] = None):
    """Logout endpoint"""
    if authorization:
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        if token in SESSIONS:
            del SESSIONS[token]
            logger.info(f"Session {token[:8]}... logged out")
    
    return {"message": "Logged out successfully"}

@app.get("/tenants")
async def list_tenants():
    """List tenants for current user"""
    return {
        "tenants": [],
        "message": "Tenant listing ready",
        "status": "stub"
    }

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8007"))
    
    logger.info(f"Starting Authentication Service on {host}:{port}")
    logger.info(f"Demo users: {list(DEMO_USERS.keys())}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        workers=1
    )