from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List

from app.dependencies import get_identity_port
from domain.ports.identity_port import IdentityPort, AuthenticatedUser

security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    token: Optional[HTTPAuthorizationCredentials] = Depends(security),
    identity: IdentityPort = Depends(get_identity_port)
) -> AuthenticatedUser:
    """
    FastAPI dependency that validates token and returns user.
    Can be used as: user: AuthenticatedUser = Depends(get_current_user)
    """
    
    # Bypass auth if configured (dev/testing)
    import os
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        return AuthenticatedUser(
            id="dev-user-id",
            email="dev@bizoholic.net",
            username="dev_admin",
            roles=["Super Admin"],
            tenant_id="default_tenant"
        )

    token_str = None
    if token:
        token_str = token.credentials
    elif request.headers.get("Authorization"):
        # Fallback manual header parsing
        parts = request.headers.get("Authorization").split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token_str = parts[1]
            
    if not token_str:
        raise HTTPException(status_code=401, detail="Missing authentication credentials")
    
    # 1. Validate Token (Introspection)
    try:
        is_valid = await identity.validate_token(token_str)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid, expired or revoked token")
    except Exception as e:
        # Log error?
        raise HTTPException(status_code=401, detail="Token validation failed")
    
    # 2. Get User Profile
    user = await identity.get_user_from_token(token_str)
    if not user:
        raise HTTPException(status_code=401, detail="Could not retrieve user profile")
    
    return user

def require_role(role: str):
    """Dependency factory for checking specific roles."""
    async def role_checker(user: AuthenticatedUser = Depends(get_current_user)):
        if role not in user.roles and "Super Admin" not in user.roles:
            raise HTTPException(status_code=403, detail=f"Missing required role: {role}")
        return user
    return role_checker
