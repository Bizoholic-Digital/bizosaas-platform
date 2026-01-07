from functools import lru_cache
import os
import logging
from domain.ports.identity_port import IdentityPort
from adapters.identity.mock_adapter import MockIdentityAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Use a default or warn
    logger.warning("DATABASE_URL not set!")
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/bizosaas"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@lru_cache()
def get_identity_port() -> IdentityPort:
    """Dependency Injection: Returns the configured Identity Adapter.
    Uses lru_cache to create a singleton instance.
    """
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        logger.info("Auth disabled: Using MockIdentityAdapter")
        return MockIdentityAdapter()

    # Clerk Configuration
    clerk_issuer = os.getenv("CLERK_ISSUER", "https://easy-kodiak-78.clerk.accounts.dev")
    
    logger.info(f"Creating ClerkAdapter with issuer {clerk_issuer}")
    
    from adapters.identity.clerk_adapter import ClerkAdapter
    return ClerkAdapter(issuer=clerk_issuer)

@lru_cache()
def get_secret_service():
    """Dependency Injection: Returns the configured Secret Service.
    Uses lru_cache to create a singleton instance.
    """
    from app.domain.services.secret_service import SecretService
    
    # Configuration
    use_vault = os.getenv("USE_VAULT", "true").lower() == "true"
    vault_addr = os.getenv("VAULT_ADDR", "http://vault:8200")
    vault_token = os.getenv("VAULT_TOKEN") # Will be None if not provided
    
    # Try Vault first if configured and token is present
    if use_vault and vault_addr and vault_token:
        try:
            from adapters.vault_adapter import VaultAdapter
            logger.info(f"Attempting to initialize Vault adapter at {vault_addr}")
            vault_adapter = VaultAdapter(
                vault_url=vault_addr,
                vault_token=vault_token,
                mount_point=os.getenv("VAULT_MOUNT_POINT", "secret")
            )
            # Only use it if authenticated
            if vault_adapter.client and vault_adapter.client.is_authenticated():
                logger.info("Successfully connected to Vault for secret storage")
                return SecretService(secret_adapter=vault_adapter)
            else:
                logger.warning("Vault initialized but not authenticated. Falling back.")
        except Exception as e:
            logger.error(f"Failed to initialize Vault: {e}")
    
    # Fallback to persistent Database storage (Safer than EnvSecretAdapter)
    from adapters.database_secret_adapter import DatabaseSecretAdapter
    logger.info("Using DatabaseSecretAdapter for persistent secret storage")
    db_adapter = DatabaseSecretAdapter(session_factory=SessionLocal)
    return SecretService(secret_adapter=db_adapter)

from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Dependency Injection: Returns the current authenticated user.
    Validates JWT tokens from the Authorization header using the configured Identity Adapter.
    """
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        from domain.ports.identity_port import AuthenticatedUser
        return AuthenticatedUser(
            id="00000000-0000-0000-0000-000000000001",
            email="system@bizosaas.local",
            name="System User",
            roles=["admin"],
            tenant_id="default"
        )

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    identity_port = get_identity_port()
    
    user = await identity_port.get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user

def require_role(allowed_roles: list[str]):
    """Factory function to create a dependency for role-based access control."""
    async def role_dependency(user = Security(get_current_user)):
        # If no roles specified, allow access (authentication is sufficient)
        if not allowed_roles:
            return user
            
        # Admin bypass
        if "admin" in user.roles:
            return user
            
        # Check if user has at least one of the allowed roles
        has_role = any(role in user.roles for role in allowed_roles)
        if not has_role:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required one of: {', '.join(allowed_roles)}",
            )
        return user
    return role_dependency

