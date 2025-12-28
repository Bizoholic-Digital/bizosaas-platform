from functools import lru_cache
import os
import logging
from domain.ports.identity_port import IdentityPort
from adapters.identity.authentik_adapter import AuthentikAdapter
from adapters.identity.mock_adapter import MockIdentityAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Use a default or warn
    logger.warning("DATABASE_URL not set!")
    DATABASE_URL = "postgresql://admin:password@localhost:5432/bizosaas_staging"

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
    
    # Check if Vault is enabled
    use_vault = os.getenv("USE_VAULT", "false").lower() == "true"
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    
    if use_vault and vault_addr and vault_token:
        try:
            from adapters.vault_adapter import VaultAdapter
            logger.info(f"Initializing Vault adapter at {vault_addr}")
            vault_adapter = VaultAdapter(
                vault_url=vault_addr,
                vault_token=vault_token,
                mount_point=os.getenv("VAULT_MOUNT_POINT", "bizosaas")
            )
            logger.info("Successfully connected to Vault for secret storage")
            return SecretService(secret_adapter=vault_adapter)
        except Exception as e:
            logger.error(f"Failed to initialize Vault: {e}")
            logger.warning("Falling back to EnvSecretAdapter")
    
    # Fallback to development adapter
    from app.adapters.env_secret_adapter import EnvSecretAdapter
    logger.warning("Using EnvSecretAdapter - secrets stored in memory (development only)")
    env_adapter = EnvSecretAdapter()
    return SecretService(secret_adapter=env_adapter)

def get_current_user():
    """Dependency Injection: Returns the current authenticated user.
    In production, this would validate JWT tokens and extract user info.
    For now, returns a default user for development/staging.
    """
    from domain.ports.identity_port import AuthenticatedUser
    
    # TODO: Implement proper JWT validation from request headers
    # For now, return a mock authenticated user for development
    return AuthenticatedUser(
        id="system-user",
        email="system@bizosaas.local",
        name="System User",
        roles=["admin"],
        tenant_id="default"
    )
