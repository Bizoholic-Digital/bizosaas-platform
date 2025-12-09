#!/usr/bin/env python3
"""
Seed script to create test users and tenants for BizOSaaS platform
"""
import asyncio
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Import from main.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import Base, User, Tenant, UserRole, TenantStatus, settings
from fastapi_users.password import PasswordHelper

# Database setup
engine = create_async_engine(
    settings.database_url,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

password_helper = PasswordHelper()

async def create_default_tenant(session: AsyncSession) -> Tenant:
    """Create default tenant"""
    # Check if tenant exists
    result = await session.execute(
        select(Tenant).where(Tenant.slug == "default")
    )
    tenant = result.scalar_one_or_none()
    
    if tenant:
        print(f"✓ Tenant 'default' already exists (ID: {tenant.id})")
        return tenant
    
    tenant = Tenant(
        name="Default Organization",
        slug="default",
        domain="localhost",
        status=TenantStatus.ACTIVE,
        subscription_plan="enterprise",
        allowed_platforms=["bizoholic", "coreldove", "bizosaas-admin"],
        max_users=100,
        features={
            "ai_agents": True,
            "crm": True,
            "cms": True,
            "analytics": True,
            "project_management": True
        }
    )
    
    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)
    
    print(f"✓ Created tenant 'default' (ID: {tenant.id})")
    return tenant

async def create_test_users(session: AsyncSession, tenant: Tenant):
    """Create test users with different roles"""
    
    users_to_create = [
        {
            "email": "admin@bizosaas.com",
            "password": "Admin@123",
            "first_name": "Super",
            "last_name": "Admin",
            "role": UserRole.SUPER_ADMIN,
            "allowed_platforms": ["bizoholic", "coreldove", "bizosaas-admin"],
            "is_superuser": True,
        },
        {
            "email": "tenant-admin@bizosaas.com",
            "password": "TenantAdmin@123",
            "first_name": "Tenant",
            "last_name": "Admin",
            "role": UserRole.TENANT_ADMIN,
            "allowed_platforms": ["bizoholic", "coreldove"],
            "is_superuser": False,
        },
        {
            "email": "user@bizosaas.com",
            "password": "User@123",
            "first_name": "Regular",
            "last_name": "User",
            "role": UserRole.USER,
            "allowed_platforms": ["bizoholic"],
            "is_superuser": False,
        },
        {
            "email": "readonly@bizosaas.com",
            "password": "ReadOnly@123",
            "first_name": "Read",
            "last_name": "Only",
            "role": UserRole.READONLY,
            "allowed_platforms": ["bizoholic"],
            "is_superuser": False,
        },
    ]
    
    created_users = []
    
    for user_data in users_to_create:
        # Check if user exists
        result = await session.execute(
            select(User).where(User.email == user_data["email"])
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"✓ User '{user_data['email']}' already exists")
            created_users.append(existing_user)
            continue
        
        # Hash password
        hashed_password = password_helper.hash(user_data["password"])
        
        # Create user
        user = User(
            email=user_data["email"],
            hashed_password=hashed_password,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            tenant_id=tenant.id,
            allowed_platforms=user_data["allowed_platforms"],
            is_active=True,
            is_verified=True,
            is_superuser=user_data["is_superuser"],
            terms_accepted_at=datetime.now(timezone.utc),
            privacy_accepted_at=datetime.now(timezone.utc),
        )
        
        session.add(user)
        created_users.append(user)
        print(f"✓ Created user '{user_data['email']}' with role {user_data['role'].value}")
    
    await session.commit()
    return created_users

async def main():
    """Main seed function"""
    print("=" * 60)
    print("BizOSaaS Platform - Database Seeding")
    print("=" * 60)
    
    async with AsyncSessionLocal() as session:
        try:
            # Create tables
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✓ Database tables created/verified")
            
            # Create default tenant
            tenant = await create_default_tenant(session)
            
            # Create test users
            users = await create_test_users(session, tenant)
            
            print("\n" + "=" * 60)
            print("✅ Seeding completed successfully!")
            print("=" * 60)
            print("\nTest Credentials:")
            print("-" * 60)
            print("Super Admin:")
            print("  Email: admin@bizosaas.com")
            print("  Password: Admin@123")
            print("\nTenant Admin:")
            print("  Email: tenant-admin@bizosaas.com")
            print("  Password: TenantAdmin@123")
            print("\nRegular User:")
            print("  Email: user@bizosaas.com")
            print("  Password: User@123")
            print("\nRead-Only User:")
            print("  Email: readonly@bizosaas.com")
            print("  Password: ReadOnly@123")
            print("-" * 60)
            print("\nLogin URL: http://localhost:3003/login")
            print("Auth API: http://localhost:8009/auth/docs")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Error during seeding: {e}")
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
