from functools import lru_cache
from typing import List, Union, Optional
import os
import logging
from domain.ports.identity_port import IdentityPort, AuthenticatedUser
from app.ports.workflow_port import WorkflowPort
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

# ============================================================================
# Database Query Profiling
# ============================================================================
from sqlalchemy import event
import time

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    # Log slow queries (above 500ms)
    if total > 0.5:
        logger.warning(f"SLOW_QUERY: {total:.4f}s - {statement}")
    
    # Record query duration in metrics if available
    try:
        from app.observability.metrics import db_query_duration
        db_query_duration.record(total * 1000) # Convert to ms
    except ImportError:
        pass

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

from fastapi import Security, HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    identity: IdentityPort = Depends(get_identity_port)
) -> AuthenticatedUser:
    """Dependency Injection: Returns the current authenticated user.
    Validates JWT tokens from the Authorization header using the configured Identity Adapter.
    """
    # Bypass auth if configured (dev/testing)
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        from domain.ports.identity_port import AuthenticatedUser
        return AuthenticatedUser(
            id="00000000-0000-0000-0000-000000000001",
            email="system@bizosaas.local",
            name="System User",
            roles=["Super Admin"],
            tenant_id="default_tenant"
        )

    token_str = None
    if credentials:
        token_str = credentials.credentials
    elif request.headers.get("Authorization"):
        # Fallback manual header parsing
        parts = request.headers.get("Authorization").split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token_str = parts[1]
    elif request.headers.get("x-clerk-auth-token"):
        # Support Clerk-injected token
        token_str = request.headers.get("x-clerk-auth-token")
            
    if not token_str:
        auth_status = request.headers.get("x-clerk-auth-status", "unknown")
        logger.error(f"DEBUG AUTH FAILURE: Headers received: {request.headers}")
        logger.error(f"DEBUG AUTH FAILURE: Clerk Auth Status: {auth_status}")
        raise HTTPException(status_code=401, detail="Missing authentication credentials")

    # 1. Validate Token (Introspection)
    try:
        is_valid = await identity.validate_token(token_str)
        if not is_valid:
            logger.error(f"DEBUG AUTH FAILURE: Token validation returned False for token: {token_str[:10]}...")
            raise HTTPException(status_code=401, detail="Invalid, expired or revoked token")
    except Exception as e:
        logger.error(f"DEBUG AUTH FAILURE: Validation Exception: {str(e)}")
        raise HTTPException(status_code=401, detail="Token validation failed")
    
    # 2. Get User Profile
    user = await identity.get_user_from_token(token_str)
    if not user:
        logger.error(f"DEBUG AUTH FAILURE: Could not retrieve user profile for token: {token_str[:10]}...")
        raise HTTPException(status_code=401, detail="Could not retrieve user profile")
    
    return user

def require_role(allowed_roles: str | List[str]):
    """Factory function to create a dependency for role-based access control.
    Supports either a single string or a list of required roles.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
        
    async def role_dependency(user = Security(get_current_user)):
        # If no roles specified, allow access (authentication is sufficient)
        if not allowed_roles:
            return user
            
        # Super Admin Bypass (Global Access)
        user_roles_lower = [r.lower() for r in user.roles]
        if "super admin" in user_roles_lower:
            return user
            
        # Check if user has at least one of the allowed roles
        allowed_roles_lower = [r.lower() for r in allowed_roles]
        has_role = any(role in user_roles_lower for role in allowed_roles_lower)
        if not has_role:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required one of: {', '.join(allowed_roles)}",
            )
        return user
    return role_dependency

@lru_cache()
def get_workflow_port() -> WorkflowPort:
    """Dependency Injection: Returns the configured Workflow Port (Temporal)."""
    from app.adapters.temporal_adapter import TemporalAdapter
    temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    
    logger.info(f"Creating TemporalAdapter for host {temporal_host}")
    return TemporalAdapter(host=temporal_host, namespace=namespace)

def get_workflow_service(
    db: Session = Depends(get_db),
    workflow_port: WorkflowPort = Depends(get_workflow_port)
):
    """Dependency Injection: Returns the Workflow Service."""
    from app.domain.services.workflow_service import WorkflowService
    return WorkflowService(db=db, workflow_port=workflow_port)

