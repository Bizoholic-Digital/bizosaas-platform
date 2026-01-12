import logging
import jwt
import os
from clerk_backend_api import Clerk
from jwt import PyJWKClient
from typing import Optional, List

from domain.ports.identity_port import IdentityPort, AuthenticatedUser

logger = logging.getLogger(__name__)

class ClerkAdapter(IdentityPort):
    """
    Clerk Authentication Adapter.
    Validates JWT tokens issued by Clerk using JWKS.
    """
    
    def __init__(self, issuer: str, audience: Optional[str] = None):
        self.issuer = issuer
        self.audience = audience
        self.jwks_url = f"{issuer}/.well-known/jwks.json"
        self.jwks_client = PyJWKClient(self.jwks_url)
        logger.info(f"ClerkAdapter initialized with issuer: {issuer}")

    async def validate_token(self, token: str) -> bool:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience,
                options={"verify_signature": True} # Default
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
        # 1. Try Local Impersonation Token
        impersonation_secret = os.getenv("IMPERSONATION_SECRET")
        if impersonation_secret:
            try:
                # Local tokens use HS256
                payload = jwt.decode(token, impersonation_secret, algorithms=["HS256"])
                if payload.get("type") == "impersonation":
                    logger.info(f"Processing impersonation token for user {payload.get('sub')}")
                    return AuthenticatedUser(
                        id=payload.get("sub"),
                        email=payload.get("email", ""),
                        name=payload.get("name", ""),
                        roles=payload.get("roles", []),
                        tenant_id=payload.get("tenant_id", "default"),
                        attributes={"impersonator_id": payload.get("impersonator_id")}
                    )
            except jwt.InvalidTokenError:
                # Not a valid local token, proceed to Clerk validation
                pass
            except Exception as e:
                logger.warning(f"Impersonation check failed: {e}")

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                issuer=self.issuer,
                audience=self.audience
            )
            
            # Map Clerk claims to AuthenticatedUser
            user_id = payload.get("sub")
            # Clerk puts email in different places depending on config.
            # Usually 'email' claim if configured, or need to look at other claims.
            # Assuming standard OIDC claims.
            email = payload.get("email") or payload.get("email_address") or ""
            
            # Clerk metadata extraction
            # Try various common keys where metadata or roles might be stored
            public_metadata = payload.get("public_metadata") or payload.get("publicMetadata") or payload.get("metadata") or {}
            
            roles = []
            # Check public_metadata
            if isinstance(public_metadata, dict):
                if "role" in public_metadata:
                    roles.append(public_metadata["role"])
                if "roles" in public_metadata:
                    if isinstance(public_metadata["roles"], list):
                        roles.extend(public_metadata["roles"])
                    else:
                        roles.append(public_metadata["roles"])
            
            # Check top-level as well (sometimes mapped by custom JWT templates)
            if "role" in payload and payload["role"] not in roles:
                roles.append(payload["role"])
            if "roles" in payload:
                payload_roles = payload["roles"]
                if isinstance(payload_roles, list):
                    for r in payload_roles:
                        if r not in roles:
                            roles.append(r)
                elif payload_roles not in roles:
                    roles.append(payload_roles)
            
            # Log payload structure if roles are still empty to help debug
            if not roles:
                logger.debug(f"No roles in JWT. Payload keys: {list(payload.keys())}")
                
                # Fallback: Fetch user from Clerk API
                clerk_secret = os.getenv("CLERK_SECRET_KEY")
                if clerk_secret and user_id:
                    try:
                        logger.info(f"Fetching user data from Clerk API for {user_id}")
                        clerk_client = Clerk(bearer_auth=clerk_secret)
                        # The clerk-backend-api is synchronous by default
                        clerk_user = clerk_client.users.get(user_id=user_id)
                        
                        if clerk_user and hasattr(clerk_user, 'public_metadata') and clerk_user.public_metadata:
                            pm = clerk_user.public_metadata
                            if isinstance(pm, dict):
                                if "role" in pm: roles.append(pm["role"])
                                if "roles" in pm: 
                                    if isinstance(pm["roles"], list): roles.extend(pm["roles"])
                                    else: roles.append(pm["roles"])
                        
                        if not roles and hasattr(clerk_user, 'private_metadata') and clerk_user.private_metadata:
                             pm = clerk_user.private_metadata
                             if isinstance(pm, dict):
                                if "role" in pm: roles.append(pm["role"])
                                if "roles" in pm:
                                    if isinstance(pm["roles"], list): roles.extend(pm["roles"])
                                    else: roles.append(pm["roles"])

                        logger.info(f"Resolved roles from Clerk API: {roles}")
                    except Exception as e:
                        logger.error(f"Clerk API fallback failed: {e}")

            tenant_id = ""
            if isinstance(public_metadata, dict):
                tenant_id = public_metadata.get("tenant_id") or public_metadata.get("tenantId")
            if not tenant_id:
                tenant_id = payload.get("tenant_id") or payload.get("tenantId") or "default"

            
            # Fallback for name
            name = payload.get("name") or email.split("@")[0]

            return AuthenticatedUser(
                id=user_id,
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
        # Simple role check for now
        # TODO: Implement granular permissions
        if "admin" in user.roles or "super_admin" in user.roles:
            return True
        return False

    async def update_user_metadata(self, user_id: str, metadata: Dict[str, Any]) -> bool:
        clerk_secret = os.getenv("CLERK_SECRET_KEY")
        if not clerk_secret:
            logger.error("CLERK_SECRET_KEY not set, cannot update metadata")
            return False
            
        try:
            clerk_client = Clerk(bearer_auth=clerk_secret)
            # update_user_metadata in clerk-backend-api
            # public_metadata is a dict
            clerk_client.users.update(
                user_id=user_id,
                public_metadata=metadata
            )
            logger.info(f"Updated Clerk metadata for user {user_id}: {metadata}")
            return True
        except Exception as e:
            logger.error(f"Failed to update Clerk metadata for {user_id}: {e}")
            return False
