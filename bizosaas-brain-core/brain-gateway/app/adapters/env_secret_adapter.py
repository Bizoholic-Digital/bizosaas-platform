import os
import logging
from typing import Dict, Any, Optional
from app.ports.secret_port import SecretPort

logger = logging.getLogger(__name__)

class EnvSecretAdapter(SecretPort):
    """
    Development adapter that uses environment variables and in-memory storage.
    NOT FOR PRODUCTION USE.
    """
    
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {}
        logger.warning("Using EnvSecretAdapter - FOR DEVELOPMENT ONLY")
    
    async def store_secret(
        self,
        path: str,
        secret_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store secret in memory (dev only)"""
        self._storage[path] = {
            "data": secret_data,
            "metadata": metadata or {}
        }
        logger.info(f"Stored secret at path: {path}")
        return True
    
    async def get_secret(self, path: str) -> Optional[Dict[str, Any]]:
        """Retrieve secret from memory"""
        secret = self._storage.get(path)
        if secret:
            return secret["data"]
        return None
    
    async def delete_secret(self, path: str) -> bool:
        """Delete secret from memory"""
        if path in self._storage:
            del self._storage[path]
            logger.info(f"Deleted secret at path: {path}")
            return True
        return False
    
    async def list_secrets(self, path_prefix: str) -> list[str]:
        """List secrets with given prefix"""
        return [
            path for path in self._storage.keys()
            if path.startswith(path_prefix)
        ]
    
    async def rotate_secret(
        self,
        path: str,
        new_secret_data: Dict[str, Any]
    ) -> bool:
        """Rotate secret (simple replacement in dev)"""
        return await self.store_secret(path, new_secret_data)
