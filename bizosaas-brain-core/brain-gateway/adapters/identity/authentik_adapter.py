import logging
import jwt
import os
import httpx
from jwt import PyJWKClient
from datetime import datetime
from typing import Optional, List, Dict, Any

from domain.ports.identity_port import IdentityPort, AuthenticatedUser

logger = logging.getLogger(__name__)

class AuthentikAdapter(IdentityPort):
    """
    Authentik Authentication Adapter.
    Validates OIDC JWT tokens issued by Authentik using JWKS.
    """
    
    def __init__(self, issuer: str, audience: Optional[str] = None):
        self.issuer = issuer
        self.audience = audience
        self.jwks_url = f"{issuer.rstrip('/')}/jwks/"
        self.jwks_client = PyJWKClient(self.jwks_url)
        # Authentik API base for administrative tasks
        # Assuming the issuer URL structure: https://auth.domain.com/application/o/slug/
        # The core API is usually at https://auth.domain.com/api/v3/
        self.api_base = issuer.split("/application/o/")[0] + "/api/v3"
        self.api_token = os.getenv("AUTHENTIK_API_TOKEN")
        logger.info(f"AuthentikAdapter initialized with issuer: {issuer}")

    async def validate_token(self, token: str) -> bool:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience,
                options={"verify_signature": True}
            )
            return True
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return False
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return False
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return False

    async def get_user_from_token(self, token: str) -> Optional[AuthenticatedUser]:
        # Support for impersonation tokens (same as Clerk implementation for compatibility)
        impersonation_secret = os.getenv("IMPERSONATION_SECRET")
        if impersonation_secret:
            try:
                payload = jwt.decode(token, impersonation_secret, algorithms=["HS256"])
                if payload.get("type") == "impersonation":
                    return AuthenticatedUser(
                        id=payload.get("sub"),
                        email=payload.get("email", ""),
                        name=payload.get("name", ""),
                        roles=payload.get("roles", []),
                        tenant_id=payload.get("tenant_id", "default"),
                        impersonator_id=payload.get("impersonator_id")
                    )
            except jwt.InvalidTokenError:
                pass

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience
            )
            
            # Authentik standard claims
            user_id = payload.get("sub")
            email = payload.get("email", "")
            name = payload.get("name") or payload.get("preferred_username") or email
            
            # Roles in Authentik usually come from 'groups' claim
            roles = payload.get("groups", [])
            
            # Extract tenant_id from custom claims or app_metadata if available
            tenant_id = payload.get("tenant_id") or payload.get("ak_tenant") or "default"
            
            return AuthenticatedUser(
                id=str(user_id),
                email=email,
                name=name,
                roles=roles,
                tenant_id=tenant_id,
                attributes=payload
            )
        except Exception as e:
            logger.error(f"Failed to get user from token: {e}")
            return None

    async def has_permission(self, user: AuthenticatedUser, permission: str) -> bool:
        # Simple RBAC based on roles/groups for now
        return permission in user.roles or "Super Admin" in user.roles or "admin" in user.roles

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """List users via Authentik API v3"""
        if not self.api_token:
            logger.warning("AUTHENTIK_API_TOKEN not set, cannot list users")
            return []
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.api_base}/core/users/",
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    params={"offset": skip, "limit": limit}
                )
                if response.status_code == 200:
                    data = response.json()
                    return data.get("results", [])
            except Exception as e:
                logger.error(f"Authentik API Error: {e}")
        return []

    async def list_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """List active sessions for a user in Authentik"""
        if not self.api_token: return []
        
        async with httpx.AsyncClient() as client:
            try:
                # Need to find the internal integer ID for the user first usually
                # Authentik sessions are under /core/authenticated_sessions/
                response = await client.get(
                    f"{self.api_base}/core/authenticated_sessions/",
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    params={"user": user_id}
                )
                if response.status_code == 200:
                    return response.json().get("results", [])
            except Exception as e:
                logger.error(f"Authentik API Error (Sessions): {e}")
        return []

    async def revoke_session(self, session_id: str) -> bool:
        """Terminate a session in Authentik"""
        if not self.api_token: return False
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{self.api_base}/core/authenticated_sessions/{session_id}/",
                    headers={"Authorization": f"Bearer {self.api_token}"}
                )
                return response.status_code == 204
            except Exception as e:
                logger.error(f"Authentik API Error (Revoke): {e}")
        return False

    async def update_user_metadata(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        """Update user attributes/metadata in Authentik"""
        if not self.api_token: return False
        
        async with httpx.AsyncClient() as client:
            try:
                # In Authentik, we update 'attributes'
                response = await client.patch(
                    f"{self.api_base}/core/users/{user_id}/",
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    json={"attributes": metadata}
                )
                return response.status_code == 200
            except Exception as e:
                logger.error(f"Authentik API Error (Update): {e}")
        return False

    async def delete_user(self, user_id: str) -> bool:
        """Permanently delete a user from Authentik"""
        if not self.api_token: return False
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(
                    f"{self.api_base}/core/users/{user_id}/",
                    headers={"Authorization": f"Bearer {self.api_token}"}
                )
                return response.status_code == 204
            except Exception as e:
                logger.error(f"Authentik API Error (Delete): {e}")
        return False

    async def change_password(self, user_id: str, new_password: str) -> bool:
        """Set a user's password in Authentik (Admin override)"""
        if not self.api_token: return False
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_base}/core/users/{user_id}/set_password/",
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    json={"password": new_password}
                )
                return response.status_code == 204 or response.status_code == 200
            except Exception as e:
                logger.error(f"Authentik API Error (Password): {e}")
        return False

    async def toggle_mfa(self, user_id: str, enabled: bool) -> bool:
        """Toggle MFA for a user by setting a custom attribute"""
        # This is a platform convention rather than a native Authentik 'toggle'
        # Authentik MFA is usually enforced by policies checking user attributes.
        return await self.update_user_metadata(user_id, {"mfa_enabled": enabled})
