import json
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app.ports.secret_port import SecretPort

logger = logging.getLogger(__name__)
Base = declarative_base()

class DBSecret(Base):
    __tablename__ = "connector_secrets"
    
    id = Column(String(255), primary_key=True)
    tenant_id = Column(String(255), index=True)
    connector_id = Column(String(255))
    secret_data = Column(Text)  # Encrypted JSON
    metadata_json = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class DatabaseSecretAdapter(SecretPort):
    """
    PostgreSQL-backed secret storage.
    Used as an alternative or fallback to Vault.
    Note: In production, secret_data should be encrypted before storage.
    """
    
    def __init__(self, session_factory):
        self.session_factory = session_factory
        # Ensure table exists
        # In a real app, use Alembic migrations instead
        from sqlalchemy import create_engine
        import os
        engine = create_engine(os.getenv("DATABASE_URL"))
        Base.metadata.create_all(engine)

    async def store_secret(self, path: str, secret_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> bool:
        session = self.session_factory()
        try:
            # Path is usually: tenants/{tenant_id}/connectors/{connector_id}
            parts = path.split("/")
            tenant_id = parts[1] if len(parts) > 1 else "unknown"
            connector_id = parts[3] if len(parts) > 3 else "unknown"

            secret = session.query(DBSecret).filter(DBSecret.id == path).first()
            if not secret:
                secret = DBSecret(id=path, tenant_id=tenant_id, connector_id=connector_id)
                session.add(secret)
            
            secret.secret_data = json.dumps(secret_data)
            secret.metadata_json = json.dumps(metadata or {})
            session.commit()
            return True
        except Exception as e:
            logger.error(f"DB Secret Store failed: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    async def get_secret(self, path: str) -> Optional[Dict[str, Any]]:
        session = self.session_factory()
        try:
            secret = session.query(DBSecret).filter(DBSecret.id == path).first()
            if secret:
                return json.loads(secret.secret_data)
            return None
        finally:
            session.close()

    async def delete_secret(self, path: str) -> bool:
        session = self.session_factory()
        try:
            secret = session.query(DBSecret).filter(DBSecret.id == path).first()
            if secret:
                session.delete(secret)
                session.commit()
                return True
            return False
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    async def list_secrets(self, path_prefix: str) -> List[str]:
        session = self.session_factory()
        try:
            secrets = session.query(DBSecret.id).filter(DBSecret.id.like(f"{path_prefix}%")).all()
            return [s.id for s in secrets]
        finally:
            session.close()

    async def rotate_secret(self, path: str, new_secret_data: Dict[str, Any]) -> bool:
        return await self.store_secret(path, new_secret_data)
