from typing import Dict, Any, Optional
import redis
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class RedisConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="redis",
            name="Redis Cloud",
            type=ConnectorType.INFRASTRUCTURE,
            description="Redis Cloud instance for caching and task queues.",
            icon="database",
            version="1.0.0",
            auth_schema={
                "url": {"type": "string", "label": "Redis URL", "placeholder": "redis://:password@host:port/db", "required": True}
            }
        )

    async def validate_credentials(self) -> bool:
        """
        Validates Redis connection strings.
        Supports url format: redis://[:password]@host:port/db
        """
        try:
            url = self.credentials.get("url")
            if not url:
                return False
            
            client = redis.from_url(url, socket_timeout=5)
            return client.ping()
        except Exception:
            return False

    async def get_status(self) -> ConnectorStatus:
        if not self.credentials:
            return ConnectorStatus.DISCONNECTED
        
        is_valid = await self.validate_credentials()
        return ConnectorStatus.CONNECTED if is_valid else ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Check Redis info for stats"""
        try:
            url = self.credentials.get("url")
            client = redis.from_url(url)
            info = client.info()
            return {
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "uptime_in_seconds": info.get("uptime_in_seconds"),
                "version": info.get("redis_version")
            }
        except Exception as e:
            return {"error": str(e)}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if action == "flushall":
            return {"status": "skipped", "message": "Flushall disabled for safety"}
        return {"error": f"Unknown action: {action}"}
