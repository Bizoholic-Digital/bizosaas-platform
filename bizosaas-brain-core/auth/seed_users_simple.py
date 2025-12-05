#!/usr/bin/env python3
"""
Seed test users for BizOSaaS Auth Service
Creates users for all roles to test the system
"""
import asyncio
import os
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi_users.password import PasswordHelper

# Import models from main.py
import sys
sys.path.insert(0, '/app')
from main import Base, User, Tenant, UserRole, TenantStatus

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@postgres:5432/bizosaas"
)

# Test users configuration
TEST_USERS = [
    {
        "email": "admin@bizosaas.com",
        "password": "Admin@123",
        "first_name": "Super",
        "last_name": "Admin",
        "role": UserRole.SUPER_ADMIN,
        "allowed_platforms": ["bizoholic", "coreldove", "bizosaas-admin", "analytics"],
    },
    {
        "email": "tenant@bizoholic.com",
        "password": "Tenant@123",
        "first_name": "Tenant",
        "last_name": "Admin",
        "role": UserRole.TENANT_ADMIN,
        "allowed_platforms": ["bizoholic"],
    },
    {
        "email": "user@bizoholic.com",
        "password": "User@123",
        "first_name": "Regular",
        "last_name": "User",
        "role": UserRole.USER,
        "allowed_platforms": ["bizoholic"],
    },
    {
        "email": "readonly@bizoholic.com",
        "password": "Readonly@123",
        "first_name": "Read",
        "last_name": "Only",
        "role": UserRole.READONLY,
        "allowed_platforms": ["bizoholic"],
    },
]

async def seed_users():
    """Seed test users into the database"""
    print(f"🌱 Seeding test users to: {DATABASE_URL}")
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    password_helper = PasswordHelper()
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if default tenant exists
            result = await session.execute(
                select(Tenant).where(Tenant.slug == "bizoholic")
            )
            tenant = result.scalar_one_or_none()
            
            if not tenant:
                print("📦 Creating default tenant: Bizoholic")
                tenant = Tenant(
                    id=uuid.uuid4(),
                    name="Bizoholic Digital",
                    slug="bizoholic",
                    domain="bizoholic.com",
                    status=TenantStatus.ACTIVE,
                    subscription_plan="enterprise",
                    allowed_platforms=["bizoholic", "coreldove", "bizosaas-admin"],
                    max_users=100,
                    features={
                        "ai_agents": True,
                        "crm": True,
                        "cms": True,
                        "ecommerce": True,
                    }
                )
                session.add(tenant)
                await session.flush()
            
            print(f"✅ Using tenant: {tenant.name} ({tenant.id})")
            
            # Create test users
            for user_data in TEST_USERS:
                # Check if user already exists
                result = await session.execute(
                    select(User).where(User.email == user_data["email"])
                )
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f"⏭️  User already exists: {user_data['email']}")
                    continue
                
                # Hash password
                hashed_password = password_helper.hash(user_data["password"])
                
                # Create user
                user = User(
                    id=uuid.uuid4(),
                    email=user_data["email"],
                    hashed_password=hashed_password,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    role=user_data["role"],
                    tenant_id=tenant.id,
                    allowed_platforms=user_data["allowed_platforms"],
                    is_active=True,
                    is_verified=True,
                    is_superuser=(user_data["role"] == UserRole.SUPER_ADMIN),
                )
                
                session.add(user)
                print(f"✅ Created user: {user.email} ({user.role})")
            
            await session.commit()
            print("\n🎉 All test users created successfully!")
            print("\n📋 Login Credentials:")
            print("=" * 60)
            for user_data in TEST_USERS:
                print(f"  {user_data['role'].value:20} | {user_data['email']:30} | {user_data['password']}")
            print("=" * 60)
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding users: {e}")
            raise
        finally:
            await session.close()
    
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_users())
