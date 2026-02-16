from functools import lru_cache
from typing import List, Union, Optional
import os
import logging
from app.domain.ports.identity_port import IdentityPort, AuthenticatedUser
from app.ports.workflow_port import WorkflowPort
from app.adapters.identity.mock_adapter import MockIdentityAdapter
from app.database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

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


@lru_cache()
def get_identity_port() -> IdentityPort:
    """Dependency Injection: Returns the configured Identity Adapter.
    Uses lru_cache to create a singleton instance.
    """
    if os.getenv("DISABLE_AUTH", "false").lower() == "true":
        logger.info("Auth disabled: Using MockIdentityAdapter")
        return MockIdentityAdapter()

    # Authentik Configuration
    authentik_issuer = os.getenv(
        "AUTHENTIK_ISSUER", 
        "https://auth-sso.bizoholic.net/application/o/bizosaas-platform/"
    )
    authentik_audience = os.getenv("AUTHENTIK_AUDIENCE")
    
    logger.info(f"Creating AuthentikAdapter with issuer {authentik_issuer}")
    
    from app.adapters.identity.authentik_adapter import AuthentikAdapter
    return AuthentikAdapter(issuer=authentik_issuer, audience=authentik_audience)

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
            from app.adapters.vault_adapter import VaultAdapter
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
    from app.adapters.database_secret_adapter import DatabaseSecretAdapter
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
        from app.domain.ports.identity_port import AuthenticatedUser
        return AuthenticatedUser(
            id="00000000-0000-0000-0000-000000000001",
            email="system@bizosaas.local",
            name="System User",
            roles=["Super Admin"],
            tenant_id="default_tenant"
        )

    token_str = None
    token_source = None
    
    if credentials:
        token_str = credentials.credentials
        token_source = "HTTPAuthorizationCredentials"
    elif request.headers.get("Authorization"):
        # Fallback manual header parsing
        parts = request.headers.get("Authorization").split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token_str = parts[1]
            token_source = "Authorization header"
    elif request.headers.get("x-clerk-auth-token"):
        # Support Clerk-injected token
        token_str = request.headers.get("x-clerk-auth-token")
        token_source = "x-clerk-auth-token header"
    elif request.cookies.get("__session"):
        # Support Clerk session cookie
        token_str = request.cookies.get("__session")
        token_source = "__session cookie"
    elif request.cookies.get("__clerk_db_jwt"):
        # Support alternate Clerk cookie
        token_str = request.cookies.get("__clerk_db_jwt")
        token_source = "__clerk_db_jwt cookie"
    
    if token_str:
        logger.info(f"AUTH: Token extracted from {token_source}")
    else:
        auth_status = request.headers.get("x-clerk-auth-status", "unknown")
        logger.error(f"AUTH FAILURE: No token found. Clerk Auth Status: {auth_status}")
        logger.error(f"AUTH FAILURE: Available cookies: {list(request.cookies.keys())}")
        logger.error(f"AUTH FAILURE: Auth-related headers: Authorization={request.headers.get('Authorization', 'None')}, x-clerk-auth-token={request.headers.get('x-clerk-auth-token', 'None')}")
        raise HTTPException(status_code=401, detail="Missing authentication credentials")

    # 1. Check for Impersonation Token
    impersonation_secret = os.getenv("IMPERSONATION_SECRET")
    if token_str and impersonation_secret:
        import jwt
        try:
            # Try to decode as an impersonation token first
            payload = jwt.decode(token_str, impersonation_secret, algorithms=["HS256"])
            if payload.get("type") == "impersonation":
                logger.info(f"Impersonation session detected: {payload.get('impersonator_id')} -> {payload.get('sub')}")
                return AuthenticatedUser(
                    id=payload["sub"],
                    email=payload["email"],
                    name=payload["name"],
                    roles=payload["roles"],
                    tenant_id=payload.get("tenant_id"),
                    impersonator_id=payload.get("impersonator_id")
                )
        except jwt.PyJWTError:
            # Not an impersonation token or invalid, continue to standard validation
            pass

    # 2. Standard Token Validation (Clerk/Auth Service)
    try:
        is_valid = await identity.validate_token(token_str)
        if not is_valid:
            logger.error(f"DEBUG AUTH FAILURE: Token validation returned False for token: {token_str[:10]}...")
            raise HTTPException(status_code=401, detail="Invalid, expired or revoked token")
    except Exception as e:
        logger.error(f"DEBUG AUTH FAILURE: Validation Exception: {str(e)}")
        raise HTTPException(status_code=401, detail="Token validation failed")
    
    # 3. Get User Profile
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

def require_feature(feature_slug: str):
    """Dependency that checks if the current user has a specific feature enabled in their plan."""
    async def feature_dependency(
        user: AuthenticatedUser = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # Admin Bypass
        user_roles_lower = [r.lower() for r in user.roles]
        if "super admin" in user_roles_lower:
            return user

        from app.services.billing_service import BillingService
        from app.models.user import User
        from app.models.billing import SubscriptionPlan
        
        # Get DB User
        db_user = db.query(User).filter(User.id == user.id).first()
        if not db_user:
             # If user doesn't exist in local DB yet, they have no features
             raise HTTPException(status_code=403, detail=f"Feature '{feature_slug}' not available. User not registered in local database.")

        # Fetch Plan Features
        billing_service = BillingService(db)
        subscription = await billing_service.get_tenant_subscription(db_user.tenant_id)
        
        plan_features = []
        if subscription:
            if hasattr(subscription, 'plan') and subscription.plan:
                plan_features = (subscription.plan.features or {}).get('feature_slugs', [])
            else:
                plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.slug == subscription.plan_id).first()
                if plan:
                    plan_features = (plan.features or {}).get('feature_slugs', [])

        if feature_slug not in plan_features:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Subscription upgrade required to access feature: {feature_slug}",
            )
        return user
    return feature_dependency

_workflow_port: Optional[WorkflowPort] = None

async def get_workflow_port() -> WorkflowPort:
    """Dependency Injection: Returns the configured Workflow Port (Temporal).
    Now asynchronous and supports mTLS if cert paths or Base64 content are provided.
    """
    global _workflow_port
    if _workflow_port is not None:
        return _workflow_port

    import base64
    from app.adapters.temporal_adapter import TemporalAdapter
    temporal_host = os.getenv("TEMPORAL_ADDRESS", "").strip() or os.getenv("TEMPORAL_HOST", "").strip() or "localhost:7233"
    namespace = os.getenv("TEMPORAL_NAMESPACE", "default").strip()
    temporal_api_key = os.getenv("TEMPORAL_API_KEY", "").strip()
    
    # Check for direct content (Base64)
    cert_content_b64 = os.getenv("TEMPORAL_MTLS_CERT_CONTENT") or os.getenv("TEMPORAL_CLIENT_CERT_CONTENT")
    key_content_b64 = os.getenv("TEMPORAL_MTLS_KEY_CONTENT") or os.getenv("TEMPORAL_CLIENT_KEY_CONTENT")
    
    # Check for file paths
    cert_path = os.getenv("TEMPORAL_MTLS_CERT") or os.getenv("TEMPORAL_CLIENT_CERT")
    key_path = os.getenv("TEMPORAL_MTLS_KEY") or os.getenv("TEMPORAL_CLIENT_KEY")
    
    cert = None
    key = None

    if cert_content_b64 and key_content_b64:
        try:
            cert = base64.b64decode(cert_content_b64)
            key = base64.b64decode(key_content_b64)
            logger.info("Loaded Temporal mTLS certs from Base64 env vars")
        except Exception as e:
            logger.error(f"Failed to decode Base64 Temporal certs: {e}")

    if not cert and cert_path and os.path.exists(cert_path):
        try:
            with open(cert_path, "rb") as f:
                cert = f.read()
                logger.info(f"Loaded Temporal client cert from {cert_path}")
        except Exception as e:
            logger.error(f"Failed to read Temporal cert at {cert_path}: {e}")

    if not key and key_path and os.path.exists(key_path):
        try:
            with open(key_path, "rb") as f:
                key = f.read()
                logger.info(f"Loaded Temporal client key from {key_path}")
        except Exception as e:
            logger.error(f"Failed to read Temporal key at {key_path}: {e}")
    
    logger.info(f"Connecting to Temporal at {temporal_host} in namespace {namespace}")
    _workflow_port = await TemporalAdapter.connect(
        host=temporal_host, 
        namespace=namespace,
        client_cert=cert,
        client_key=key,
        api_key=temporal_api_key
    )
    return _workflow_port

def get_workflow_service(
    db: Session = Depends(get_db),
    workflow_port: WorkflowPort = Depends(get_workflow_port)
):
    """Dependency Injection: Returns the Workflow Service."""
    from app.domain.services.workflow_service import WorkflowService
    return WorkflowService(db=db, workflow_port=workflow_port)

def get_connector_service(secret_service = Depends(get_secret_service)):
    """Dependency Injection: Returns the Connector Service."""
    from app.domain.services.connector_service import ConnectorService
    return ConnectorService(secret_service=secret_service)

def get_audit_service(db: Session = Depends(get_db)):
    """Dependency Injection: Returns the Audit Service."""
    from app.services.audit_service import AuditService
    return AuditService(db)

