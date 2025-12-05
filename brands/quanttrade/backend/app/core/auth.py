"""
Authentication and authorization utilities
"""

from typing import Dict, Any, Optional
from fastapi import HTTPException, status, Depends, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import structlog

from core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

security = HTTPBearer()


async def get_current_user() -> Dict[str, Any]:
    """Mock authentication - replace with real implementation"""
    return {
        "id": "user_123",
        "user_id": "user_123",
        "username": "demo_trader",
        "email": "demo@quanttrade.com",
        "is_active": True,
        "is_premium": True,
        "permissions": ["read", "write", "trade", "backtest"]
    }


async def get_current_user_ws(websocket: WebSocket) -> Optional[Dict[str, Any]]:
    """WebSocket authentication - mock implementation"""
    # In production, extract token from WebSocket headers or query params
    # For now, return a mock user
    return {
        "id": "user_123",
        "user_id": "user_123",
        "username": "demo_trader",
        "email": "demo@quanttrade.com",
        "is_active": True,
        "is_premium": True,
        "permissions": ["read", "write", "trade", "backtest"]
    }


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify JWT token - mock implementation"""
    try:
        # In production, decode and verify JWT token
        token = credentials.credentials

        # Mock verification
        if token == "demo_token":
            return await get_current_user()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_permissions(user: Dict[str, Any], required_permission: str) -> bool:
    """Check if user has required permission"""
    user_permissions = user.get("permissions", [])
    return required_permission in user_permissions


def require_permission(permission: str):
    """Decorator to require specific permission"""
    async def permission_dependency(user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        if not check_permissions(user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return user

    return permission_dependency


# Common permission dependencies
require_read = require_permission("read")
require_write = require_permission("write")
require_trade = require_permission("trade")
require_backtest = require_permission("backtest")