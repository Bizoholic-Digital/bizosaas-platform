import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi_users.password import PasswordHelper

# Database Config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/bizosaas")

# Password to set
NEW_PASSWORD = "AdminDemo2024!"
EMAIL = "admin@bizoholic.com"

async def reset_password():
    print(f"Connecting to database: {DATABASE_URL}")
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if user exists
        result = await session.execute(text("SELECT id, email, hashed_password FROM users WHERE email = :email"), {"email": EMAIL})
        user = result.fetchone()

        if not user:
            print(f"User {EMAIL} not found!")
            # Create user if not exists? No, better to fail and report.
            return

        print(f"User found: {user.email}")
        
        # Hash new password
        helper = PasswordHelper()
        hashed_password = helper.hash(NEW_PASSWORD)
        
        # Update password
        await session.execute(
            text("UPDATE users SET hashed_password = :password WHERE email = :email"),
            {"password": hashed_password, "email": EMAIL}
        )
        await session.commit()
        print(f"Password for {EMAIL} has been reset to: {NEW_PASSWORD}")

if __name__ == "__main__":
    asyncio.run(reset_password())
