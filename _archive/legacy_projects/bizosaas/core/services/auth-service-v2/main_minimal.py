#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import asyncio
import os
import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import asyncpg
import redis.asyncio as redis

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Bizoholic2024Alagiri@postgres:5432/bizosaas")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/1")
JWT_SECRET = os.getenv("JWT_SECRET", "bizosaas-central-secret-key")
SECRET_KEY = os.getenv("SECRET_KEY", "auth-service-secret-key-production")

app = FastAPI(
    title="BizOSaaS Auth Service v2",
    description="Authentication service for BizOSaaS platform",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    tenant_name: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    full_name: str
    tenant_id: Optional[str] = None

# Global connections
db_pool: Optional[asyncpg.Pool] = None
redis_client: Optional[redis.Redis] = None
security = HTTPBearer()

@app.on_event("startup")
async def startup():
    global db_pool, redis_client
    
    # Database connection
    db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    
    # Redis connection
    redis_client = redis.from_url(REDIS_URL)
    
    # Create basic tables if they don't exist
    async with db_pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                salt VARCHAR(255) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                tenant_id INTEGER,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                domain VARCHAR(255),
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(255) UNIQUE NOT NULL,
                user_id INTEGER REFERENCES users(id),
                tenant_id INTEGER REFERENCES tenants(id),
                expires_at TIMESTAMP NOT NULL,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

@app.on_event("shutdown")
async def shutdown():
    global db_pool, redis_client
    if db_pool:
        await db_pool.close()
    if redis_client:
        await redis_client.close()

# Auth utilities
def hash_password(password: str) -> tuple[str, str]:
    salt = secrets.token_hex(32)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return password_hash.hex(), salt

def verify_password(password: str, password_hash: str, salt: str) -> bool:
    calculated_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return calculated_hash.hex() == password_hash

def create_jwt_token(user_data: Dict[str, Any]) -> str:
    payload = {
        'user_id': str(user_data['id']),
        'email': user_data['email'],
        'tenant_id': str(user_data.get('tenant_id', '')),
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow(),
        'sub': user_data['email']
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.PyJWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

# API Endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth-service-v2", "timestamp": datetime.utcnow()}

@app.post("/auth/register", response_model=AuthResponse)
async def register(user_data: UserRegister):
    async with db_pool.acquire() as conn:
        # Check if user exists
        existing_user = await conn.fetchrow(
            "SELECT id FROM users WHERE email = $1", user_data.email
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create tenant if provided
        tenant_id = None
        if user_data.tenant_name:
            tenant_id = await conn.fetchval(
                "INSERT INTO tenants (name) VALUES ($1) RETURNING id",
                user_data.tenant_name
            )
        
        # Hash password
        password_hash, salt = hash_password(user_data.password)
        
        # Create user
        user_id = await conn.fetchval("""
            INSERT INTO users (email, password_hash, salt, full_name, tenant_id)
            VALUES ($1, $2, $3, $4, $5) RETURNING id
        """, user_data.email, password_hash, salt, user_data.full_name, tenant_id)
        
        # Create JWT token
        user_dict = {
            'id': user_id,
            'email': user_data.email,
            'full_name': user_data.full_name,
            'tenant_id': tenant_id
        }
        
        access_token = create_jwt_token(user_dict)
        
        return AuthResponse(
            access_token=access_token,
            user_id=str(user_id),
            email=user_data.email,
            full_name=user_data.full_name,
            tenant_id=str(tenant_id) if tenant_id else None
        )

@app.post("/auth/login", response_model=AuthResponse)
async def login(login_data: UserLogin):
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow("""
            SELECT id, email, password_hash, salt, full_name, tenant_id, is_active
            FROM users WHERE email = $1
        """, login_data.email)
        
        if not user or not user['is_active']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(login_data.password, user['password_hash'], user['salt']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Update last login
        await conn.execute(
            "UPDATE users SET updated_at = NOW() WHERE id = $1",
            user['id']
        )
        
        # Create JWT token
        access_token = create_jwt_token(dict(user))
        
        return AuthResponse(
            access_token=access_token,
            user_id=str(user['id']),
            email=user['email'],
            full_name=user['full_name'],
            tenant_id=str(user['tenant_id']) if user['tenant_id'] else None
        )

@app.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user['user_id'],
        "email": current_user['email'],
        "tenant_id": current_user.get('tenant_id')
    }

@app.post("/auth/refresh")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow("""
            SELECT id, email, full_name, tenant_id, is_active
            FROM users WHERE id = $1
        """, int(current_user['user_id']))
        
        if not user or not user['is_active']:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        access_token = create_jwt_token(dict(user))
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

@app.post("/auth/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    # In a real implementation, you'd invalidate the token in Redis
    # For now, we'll just return success
    return {"message": "Logged out successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)