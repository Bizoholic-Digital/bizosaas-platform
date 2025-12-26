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

    # Default to localhost for dev, but in Docker it should be container name
    authentik_url = os.getenv("AUTHENTIK_URL", "http://authentik-server:9000")
    client_id = os.getenv("AUTHENTIK_CLIENT_ID", "bizosaas-brain")
    client_secret = os.getenv("AUTHENTIK_CLIENT_SECRET", "dev-secret")
    
    logger.info(f"Creating AuthentikAdapter for {authentik_url}")
    
    return AuthentikAdapter(
        authentik_url=authentik_url,
        client_id=client_id,
        client_secret=client_secret
    )

@lru_cache()
def get_secret_service():
    """Dependency Injection: Returns the configured Secret Service.
    Uses lru_cache to create a singleton instance.
    """
    from adapters.vault_adapter import VaultAdapter
    from app.domain.services.secret_service import SecretService
    
    # Check if Vault is enabled
    use_vault = os.getenv("USE_VAULT", "true").lower() == "true"
    
    if not use_vault:
        logger.warning("Vault disabled - using mock secret storage")
        # TODO: Implement MockSecretAdapter for development
        from adapters.vault_adapter import VaultAdapter
        vault_adapter = VaultAdapter()
    else:
        vault_adapter = VaultAdapter()
    
    return SecretService(secret_adapter=vault_adapter)

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
