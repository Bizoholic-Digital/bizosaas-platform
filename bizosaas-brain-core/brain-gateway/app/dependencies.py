from functools import lru_cache
import os
import logging
from domain.ports.identity_port import IdentityPort
from adapters.identity.authentik_adapter import AuthentikAdapter

logger = logging.getLogger(__name__)

@lru_cache()
def get_identity_port() -> IdentityPort:
    """Dependency Injection: Returns the configured Identity Adapter.
    Uses lru_cache to create a singleton instance.
    """
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
