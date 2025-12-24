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
