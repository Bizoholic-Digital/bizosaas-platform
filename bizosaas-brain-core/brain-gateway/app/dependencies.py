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
        id="00000000-0000-0000-0000-000000000001",  # Valid UUID
        email="system@bizosaas.local",
        name="System User",
        roles=["admin"],
        tenant_id="default"  # Consistent with seeding
    )

_temporal_adapter = None

async def get_workflow_service():
    """Dependency Injection: Returns the configured Temporal Workflow Adapter.
    Initializes connection on first use (Singleton).
    """
    global _temporal_adapter
    if _temporal_adapter:
        return _temporal_adapter
        
    from app.adapters.temporal_adapter import TemporalAdapter
    
    host = os.getenv("TEMPORAL_HOST", "temporal:7233")
    namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    cert_content = os.getenv("TEMPORAL_MTLS_CERT")
    key_content = os.getenv("TEMPORAL_MTLS_KEY")
    
    # Try to load from Connector Registry (via Vault)
    # This allows updating credentials via Admin UI without redeploying
    try:
        secret_service = get_secret_service()
        # Default tenant for system-wide Temporal
        creds = await secret_service.get_connector_credentials("default", "temporal")
        
        if creds:
            logger.info("Found configured Temporal connector credentials in Vault")
            host = creds.get("host", host)
            namespace = creds.get("namespace", namespace)
            cert_content = creds.get("tls_cert", cert_content)
            key_content = creds.get("tls_key", key_content)
    except Exception as e:
        logger.warning(f"Could not load Temporal credentials from Vault: {e}")

    cert_bytes = None
    key_bytes = None
    
    # Helper to load content from file path or string
    def load_content(val):
        if not val:
            return None
        # If it looks like a file path and exists, read it
        if "/" in val and os.path.exists(val):
            try:
                with open(val, "rb") as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Failed to read cert file {val}: {e}")
                return None
        # Otherwise assume it's the PEM content string
        return val.encode('utf-8')

    if cert_content and key_content:
        cert_bytes = load_content(cert_content)
        key_bytes = load_content(key_content)
    
    try:
        _temporal_adapter = await TemporalAdapter.connect(
            host=host, 
            namespace=namespace,
            tls_cert=cert_bytes, 
            tls_key=key_bytes
        )
        return _temporal_adapter
    except Exception as e:
        logger.error(f"Failed to connect to Temporal: {e}")
        return None
