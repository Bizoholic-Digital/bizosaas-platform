import httpx
import logging
import os
from typing import Optional, List, Dict, Any
from domain.ports.identity_port import IdentityPort, AuthenticatedUser

logger = logging.getLogger("authentik_adapter")

class AuthentikAdapter(IdentityPort):
    """Adapter that implements IdentityPort using Authentik OIDC Protocol.
    
    Configuration comes from Environment Variables or Injection.
    """
    
    def __init__(self, authentik_url: str, client_id: str, client_secret: str, realm: str = "bizosaas"):
        self.authentik_url = authentik_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.realm = realm
        # Standard OIDC endpoints in Authentik
        self.token_introspection_url = f"{self.authentik_url}/application/o/introspect/"
        self.userinfo_url = f"{self.authentik_url}/application/o/userinfo/"
        
        logger.info(f"Initialized AuthentikAdapter at {self.authentik_url}")

    async def validate_token(self, token: str) -> bool:
        """
        Validates token via OIDC Introspection. 
        Better than local validation as it checks for revocation.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.token_introspection_url,
                    data={
                        "token": token,
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                    },
                    timeout=5.0
                )
                if response.status_code == 200:
                    data = response.json()
                    # 'active' boolean is standard OAuth2 introspection response
                    is_active = data.get("active", False)
                    if not is_active:
                        logger.debug("Token introspection returned inactive")
                    return is_active
                
                logger.error(f"Authentik Introspection failed: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error validating token: {str(e)}")
            return False

    async def get_user_from_token(self, token: str) -> Optional[AuthenticatedUser]:
        """
        Fetches user profile via OIDC UserInfo endpoint.
        Maps Authentik claims to Domain Entity.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.userinfo_url,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Authentik specific mappings
                    # 'groups' claim contains group names (Roles)
                    # 'sub' is the unique Subject ID
                    
                    user = AuthenticatedUser(
                        id=data.get("sub"),
                        email=data.get("email"),
                        name=data.get("name", data.get("preferred_username", "Unknown")),
                        roles=data.get("groups", []),
                        # Authentik stores custom attributes in 'attributes' or flat claims?
                        # It depends on Scope mapping. We assume flat or 'attributes'
                        attributes=data,
                        # Check for tenant_id in generic attributes if available
                        tenant_id=data.get("tenant_id") or data.get("attributes", {}).get("tenant_id")
                    )
                    
                    # Map permissions from groups/roles if possible, otherwise leave empty
                    # (Permission logic usually requires a separate sync or claim)
                    
                    return user
                
                logger.error(f"Authentik UserInfo failed: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error fetching user from token: {str(e)}")
            return None

    async def has_permission(self, user: AuthenticatedUser, permission: str) -> bool:
        """
        Checks permission. In Authentik, this maps to 'permissions' claim or Group membership.
        Currently simple check against 'roles' or explicit permissions list.
        """
        # 1. Direct permission check
        if permission in user.permissions:
            return True
        
        # 2. Role-based permission (Super Admin has all)
        if "Super Admin" in user.roles or "admin" in user.roles:
            return True
            
        return False
