"""
Simple authentication endpoints for Client Portal
This module provides authentication endpoints to be imported into the main FastAPI app
"""
from fastapi import HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import time
import base64
import logging

logger = logging.getLogger(__name__)

# Demo user for development
DEMO_USERS = {
    "demo@bizosaas.com": {
        "id": "user_demo_001",
        "email": "demo@bizosaas.com",
        "password": "demo123",
        "name": "Demo User",
        "role": "admin",
        "tenant_id": "tenant_demo"
    }
}

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def setup_auth_endpoints(app):
    """Register authentication endpoints on the provided FastAPI app"""

    @app.post("/api/auth/login")
    async def login(request: LoginRequest):
        """Authentication endpoint for Client Portal login"""
        try:
            user_data = DEMO_USERS.get(request.email)

            if not user_data or user_data["password"] != request.password:
                return {"success": False, "error": "Invalid email or password"}

            # Generate simple token
            token_data = {
                "user_id": user_data["id"],
                "email": user_data["email"],
                "tenant_id": user_data["tenant_id"],
                "exp": int(time.time()) + 86400
            }
            token = base64.b64encode(json.dumps(token_data).encode()).decode()

            return {
                "success": True,
                "token": token,
                "user": {
                    "id": user_data["id"],
                    "email": user_data["email"],
                    "name": user_data["name"],
                    "role": user_data["role"],
                    "tenant_id": user_data["tenant_id"]
                }
            }

        except Exception as e:
            logger.error(f"Login error: {e}")
            return {"success": False, "error": "Authentication service error"}

    @app.post("/api/auth/logout")
    async def logout():
        return {"success": True, "message": "Logged out successfully"}

    @app.get("/api/auth/me")
    async def get_current_user(authorization: Optional[str] = Header(None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="No authorization token")

        try:
            token = authorization.split(" ")[1]
            token_data = json.loads(base64.b64decode(token).decode())

            if token_data.get("exp", 0) < time.time():
                raise HTTPException(status_code=401, detail="Token expired")

            return {
                "success": True,
                "user": {
                    "id": token_data["user_id"],
                    "email": token_data["email"],
                    "tenant_id": token_data["tenant_id"]
                }
            }

        except Exception as e:
            logger.error(f"Token validation error: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
