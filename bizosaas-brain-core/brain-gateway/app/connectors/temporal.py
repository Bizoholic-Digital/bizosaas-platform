from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from app.adapters.temporal_adapter import TemporalAdapter
import logging

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class TemporalConnector(BaseConnector):
    """
    Connector for Temporal Cloud Workflow Orchestration.
    """

    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="temporal",
            name="Temporal Cloud",
            type=ConnectorType.TASK_MANAGEMENT,
            description="Connect to Temporal Cloud for durable workflow orchestration",
            icon="https://temporal.io/favicon.ico",
            version="1.0.0",
            auth_schema={
                "type": "object",
                "properties": {
                    "host": {
                        "type": "string", 
                        "title": "Temporal Host",
                        "description": "e.g., namespace.id.tmprl.cloud:7233",
                        "default": "temporal.key.tmprl.cloud:7233"
                    },
                    "namespace": {
                        "type": "string",
                        "title": "Namespace",
                        "default": "default"
                    },
                    "api_key": {
                        "type": "string",
                        "title": "API Key (Optional)",
                        "description": "For Control Plane operations (if supported)"
                    },
                    "tls_cert": {
                        "type": "string",
                        "title": "Client Certificate (PEM)",
                        "format": "textarea",
                        "description": "Required for Cloud Data Plane (mTLS)"
                    },
                    "tls_key": {
                        "type": "string",
                        "title": "Private Key (PEM)",
                        "format": "textarea",
                        "description": "Required for Cloud Data Plane (mTLS)"
                    }
                },
                "required": ["host", "namespace"]
            }
        )

    async def validate_credentials(self) -> bool:
        """
        Validate by attempting to connect to the Temporal server.
        """
        try:
            host = self.credentials.get("host")
            namespace = self.credentials.get("namespace")
            tls_cert = self.credentials.get("tls_cert")
            tls_key = self.credentials.get("tls_key")
            
            # Convert string credentials to bytes if present
            cert_bytes = tls_cert.encode('utf-8') if tls_cert else None
            key_bytes = tls_key.encode('utf-8') if tls_key else None
            
            # Attempt connection
            adapter = await TemporalAdapter.connect(
                host=host, 
                namespace=namespace, 
                tls_cert=cert_bytes, 
                tls_key=key_bytes
            )
            
            # If we get here, connection was successful
            # We can verify further by checking client status or listing something
            # For now, connection establishment is a good check.
            
            logger.info(f"Successfully validated Temporal connection to {host}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate Temporal credentials: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        # Simple check - if we can validate, we are connected
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Placeholder: Could list running workflows or schedules.
        """
        return {"message": "Sync not implemented for Temporal yet"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Placeholder: Could trigger workflows externally.
        """
        return {"status": "success", "message": f"Action {action} received"}
