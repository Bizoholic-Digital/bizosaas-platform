from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from datetime import datetime, timedelta, timezone
import uuid
import os
from jose import jwt
from typing import Optional

# Import DB session dependency from main (circular import avoidance might be needed, 
# but usually dependency injection handles it if we import the function)
# For now, we'll assume we can import get_async_session from main or define a local one if needed.
# Better to import the engine/sessionmaker from a shared database module if available, 
# but checking main.py shows it's all in one file. 
# We will need to be careful about imports.

# Define Models locally to avoid Pydantic conflicts
class ExchangeRequest(BaseModel):
    email: str
    provider: str
    secret: str
    platform: str = "bizoholic"
    name: Optional[str] = None
    avatar_url: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict
    tenant: dict

router = APIRouter()

# Configuration (should match main.py)
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
NEXTAUTH_SECRET = os.getenv("NEXTAUTH_SECRET", "your-super-secret-nextauth-key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Dependency placeholder
async def get_db_session():
    return None

@router.post("/auth/token/exchange", response_model=TokenResponse)
async def token_exchange(
    request: ExchangeRequest,
    db_session: AsyncSession = Depends(get_db_session)
):
    # 1. Verify Secret
    if request.secret != NEXTAUTH_SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")

    # 2. Database Logic (Raw SQL or ORM)
    # We'll use raw SQL for maximum stability if ORM models are flaky, 
    # but let's try ORM first if we can import models safely.
    # Since models are in main.py, importing them might cause circular imports.
    # Strategy: Use raw SQL for the exchange to be 100% safe from Pydantic/ORM model crashes.
    
    try:
        # Check for user
        result = await db_session.execute(
            text("SELECT id, email, tenant_id, role FROM users WHERE email = :email"),
            {"email": request.email}
        )
        user = result.first()

        tenant_id = None
        user_id = None
        role = "user"

        if not user:
            # JIT Provisioning
            # Find demo tenant
            tenant_result = await db_session.execute(
                text("SELECT id FROM tenants WHERE slug = 'demo'")
            )
            tenant = tenant_result.first()
            
            if not tenant:
                # Create tenant
                tenant_id = uuid.uuid4()
                await db_session.execute(
                    text("INSERT INTO tenants (id, name, slug, status, created_at, updated_at, max_users, allowed_platforms, api_rate_limit) VALUES (:id, 'Demo Tenant', 'demo', 'active', NOW(), NOW(), 10, '[]', 1000)"),
                    {"id": tenant_id}
                )
            else:
                tenant_id = tenant[0]

            # Create User
            user_id = uuid.uuid4()
            await db_session.execute(
                text("INSERT INTO users (id, email, hashed_password, is_active, is_verified, is_superuser, tenant_id, role, login_count, failed_login_attempts, two_factor_enabled, marketing_consent) VALUES (:id, :email, 'oauth_user', true, true, false, :tenant_id, 'user', 0, 0, false, false)"),
                {"id": user_id, "email": request.email, "tenant_id": tenant_id}
            )
            await db_session.commit()
        else:
            user_id = user[0]
            tenant_id = user[2]
            role = user[3] # This is a string in DB

        # 3. Generate JWT
        expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),
            "email": request.email,
            "role": role,
            "tenant_id": str(tenant_id),
            "exp": expires,
            "platform": request.platform
        }
        access_token = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
        refresh_token = str(uuid.uuid4()) # Simple refresh token

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {"id": str(user_id), "email": request.email, "role": role},
            "tenant": {"id": str(tenant_id)}
        }

    except Exception as e:
        print(f"Exchange Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
