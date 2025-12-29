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
    elif request.headers.get("x-clerk-auth-token"):
        # Support Clerk-injected token
        token_str = request.headers.get("x-clerk-auth-token")
            
    if not token_str:
        import logging
        auth_status = request.headers.get("x-clerk-auth-status", "unknown")
        logging.error(f"DEBUG AUTH FAILURE: Headers received: {request.headers}")
        logging.error(f"DEBUG AUTH FAILURE: Clerk Auth Status: {auth_status}")
        raise HTTPException(status_code=401, detail="Missing authentication credentials")

    
    # 1. Validate Token (Introspection)
    try:
        is_valid = await identity.validate_token(token_str)
        if not is_valid:
            import logging
            logging.error(f"DEBUG AUTH FAILURE: Token validation returned False for token: {token_str[:10]}...")
            raise HTTPException(status_code=401, detail="Invalid, expired or revoked token")
    except Exception as e:
        import logging
        logging.error(f"DEBUG AUTH FAILURE: Validation Exception: {str(e)}")
        raise HTTPException(status_code=401, detail="Token validation failed")
    
    # 2. Get User Profile
    user = await identity.get_user_from_token(token_str)
    if not user:
        import logging
        logging.error(f"DEBUG AUTH FAILURE: Could not retrieve user profile for token: {token_str[:10]}...")
        raise HTTPException(status_code=401, detail="Could not retrieve user profile")
    
    import logging
    logging.info(f"DEBUG AUTH SUCCESS: User {user.id} authenticated with roles: {user.roles}")
    return user


def require_role(role: str):
    """Dependency factory for checking specific roles.
    Matches the requested role or any super-admin level role.
    """
    async def role_checker(user: AuthenticatedUser = Depends(get_current_user)):
        # Normalize requested role and user roles
        req_role_lower = role.lower()
        user_roles_lower = [r.lower() for r in user.roles]
        
        # Super-admin level roles that bypass any specific role check
        admin_roles = ["super admin", "super_admin", "platform administrator", "platform_administrator", "admin"]
        
        # Check for direct match
        if req_role_lower in user_roles_lower:
            return user
            
        # Check if user has any of the admin roles
        has_admin_privilege = any(admin_role in user_roles_lower for admin_role in admin_roles)
        
        if has_admin_privilege:
            return user
            
        raise HTTPException(
            status_code=403, 
            detail=f"Missing required role: {role}. User roles: {user.roles}"
        )
    return role_checker

