#!/usr/bin/env python3
"""
Seed Test Users for BizOSaaS Unified Auth
Creates test users with proper password hashing
"""

import asyncio
import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncpg
from passlib.context import CryptContext

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

import os

# Database URL (use localhost since running from host, not container)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas")

# Test credentials from ~/projects/credentials.md
# Note: Schema uses email for login, not username
TEST_USERS = [
    # Super Admins (Platform Level)
    {
        "email": "admin@bizoholic.com",
        "password": "AdminDemo2024!",
        "role": "super_admin",
        "first_name": "Admin",
        "last_name": "Demo"
    },
    {
        "email": "superadmin@bizosaas.com",
        "password": "BizoSaaS2025!Admin",
        "role": "super_admin",
        "first_name": "Super",
        "last_name": "Admin"
    },
    
    # Admins (Tenant Level)
    {
        "email": "admin@test.com",
        "password": "Admin2024!Test",
        "role": "admin",
        "first_name": "Admin",
        "last_name": "User"
    },
    {
        "email": "administrator@bizosaas.com",
        "password": "Bizoholic2025!Admin",
        "role": "admin",
        "first_name": "Tenant",
        "last_name": "Admin"
    },
    
    # Managers
    {
        "email": "manager@test.com",
        "password": "Manager2024!Test",
        "role": "manager",
        "first_name": "Manager",
        "last_name": "User"
    },
    
    # Regular Users
    {
        "email": "user@bizosaas.com",
        "password": "Bizoholic2025!User",
        "role": "user",
        "first_name": "Test",
        "last_name": "User"
    },
    {
        "email": "user@test.com",
        "password": "User2024!Test",
        "role": "user",
        "first_name": "Regular",
        "last_name": "User"
    },
    
    # Clients
    {
        "email": "client@bizosaas.com",
        "password": "ClientDemo2024!",
        "role": "client",
        "first_name": "Client",
        "last_name": "Demo"
    },
    {
        "email": "client@test.com",
        "password": "Client2024!Test",
        "role": "client",
        "first_name": "Test",
        "last_name": "Client"
    },
    
    # Additional Role Tests
    {
        "email": "viewer@test.com",
        "password": "Viewer2024!Test",
        "role": "viewer",
        "first_name": "View",
        "last_name": "Only"
    }
]

async def create_test_users():
    """Create test users with proper password hashing"""

    # Create async engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        try:
            # First, create a default tenant
            tenant_id = str(uuid.uuid4())

            # Check if tenant exists
            result = await session.execute(
                text("SELECT id FROM tenants WHERE slug = 'bizosaas-admin' LIMIT 1")
            )
            existing_tenant = result.fetchone()

            if existing_tenant:
                tenant_id = str(existing_tenant[0])
                print(f"✅ Using existing tenant: {tenant_id}")
            else:
                # Create tenant with all required fields
                await session.execute(
                    text("""
                        INSERT INTO tenants (id, name, slug, status, created_at, updated_at, max_users, api_rate_limit)
                        VALUES (:id, :name, :slug, :status, :created_at, :updated_at, :max_users, :api_rate_limit)
                    """),
                    {
                        "id": tenant_id,
                        "name": "BizOSaaS Admin Tenant",
                        "slug": "bizosaas-admin",
                        "status": "active",
                        "created_at": datetime.now(timezone.utc),
                        "updated_at": datetime.now(timezone.utc),
                        "max_users": 1000,
                        "api_rate_limit": 10000  # 10,000 requests per hour for test tenant
                    }
                )
                await session.commit()
                print(f"✅ Created tenant: {tenant_id}")

            # Create test users
            for user_data in TEST_USERS:
                user_id = str(uuid.uuid4())
                hashed_password = pwd_context.hash(user_data["password"])

                # Check if user already exists
                result = await session.execute(
                    text("SELECT id FROM users WHERE email = :email LIMIT 1"),
                    {"email": user_data["email"]}
                )
                existing_user = result.fetchone()

                if existing_user:
                    print(f"⚠️  User {user_data['email']} already exists, skipping...")
                    continue

                # Insert user (all required fields from schema)
                await session.execute(
                    text("""
                        INSERT INTO users (
                            id, email, hashed_password, role,
                            tenant_id, first_name, last_name,
                            is_active, is_verified, is_superuser,
                            login_count, failed_login_attempts,
                            two_factor_enabled, marketing_consent
                        )
                        VALUES (
                            :id, :email, :hashed_password, :role,
                            :tenant_id, :first_name, :last_name,
                            :is_active, :is_verified, :is_superuser,
                            :login_count, :failed_login_attempts,
                            :two_factor_enabled, :marketing_consent
                        )
                    """),
                    {
                        "id": user_id,
                        "email": user_data["email"],
                        "hashed_password": hashed_password,
                        "role": user_data["role"],
                        "tenant_id": tenant_id,
                        "first_name": user_data["first_name"],
                        "last_name": user_data["last_name"],
                        "is_active": True,
                        "is_verified": True,
                        "is_superuser": user_data["role"] == "super_admin",
                        "login_count": 0,
                        "failed_login_attempts": 0,
                        "two_factor_enabled": False,
                        "marketing_consent": False
                    }
                )
                await session.commit()

                print(f"✅ Created user: {user_data['email']} ({user_data['role']})")
                print(f"   Password: {user_data['password']}")
                print()

            print("\n🎉 Test users created successfully!")
            print("\nYou can now login with:")
            print("-" * 60)
            for user_data in TEST_USERS:
                print(f"\n{user_data['role'].upper()}:")
                print(f"  Email: {user_data['email']}")
                print(f"  Password: {user_data['password']}")
            print("-" * 60)

        except Exception as e:
            await session.rollback()
            print(f"❌ Error creating test users: {e}")
            raise
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_test_users())