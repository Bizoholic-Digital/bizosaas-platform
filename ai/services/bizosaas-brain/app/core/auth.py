"""
Authentication utilities for Brain API
"""

from typing import Optional
from fastapi import HTTPException, Depends, Header

class User:
    """Simple user model for analytics"""
    def __init__(self, id: int, username: str, tenant_id: str):
        self.id = id
        self.username = username
        self.tenant_id = tenant_id

async def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Get current user from authorization header"""
    # For development/testing, return a mock user
    # In production, this would decode JWT and validate
    return User(id=1, username="admin", tenant_id="demo")

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    return current_user