from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class ConnectorType(str, Enum):
    CMS = "cms"
    CRM = "crm"
    ECOMMERCE = "ecommerce"
    ANALYTICS = "analytics"
    MARKETING = "marketing"
    COMMUNICATION = "communication"
    BILLING = "billing"
    TASK_MANAGEMENT = "task_management"
    PROJECT_MANAGEMENT = "project_management"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"


class ConnectorStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    PENDING = "pending"
    DEGRADED = "degraded"

class ConnectorConfig(BaseModel):
    id: str
    name: str
    type: ConnectorType
    description: str
    icon: str
    version: str = "1.0.0"
    capabilities: List[Union[ConnectorType, str]] = []  # List of what this connector provides
    auth_schema: Dict[str, Any]  # JSON schema for required credentials

class BaseConnector(ABC):
    """
    Abstract base class for all BizOSaaS Connectors.
    Enables plug-and-play integration with external platforms.
    """
    
    def __init__(self, tenant_id: str, credentials: Dict[str, Any]):
        self.tenant_id = tenant_id
        self.credentials = credentials
        self.logger = logging.getLogger(f"connector.{self.config.id}.{tenant_id}")

    @classmethod
    @abstractmethod
    def get_config(cls) -> ConnectorConfig:
        """Return the configuration metadata for this connector class"""
        pass

    @property
    def config(self) -> ConnectorConfig:
        """Instance convenience accessor for config"""
        return self.get_config()

    @abstractmethod
    async def validate_credentials(self) -> bool:
        """
        Verify that the provided credentials are valid.
        Should make a lightweight API call to the external service.
        """
        pass

    @abstractmethod
    async def get_status(self) -> ConnectorStatus:
        """
        Check the current health status of the connection.
        """
        pass

    @abstractmethod
    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch data from the external platform.
        
        Args:
            resource_type: The type of data to fetch (e.g., 'posts', 'contacts')
            params: Optional filtering or pagination parameters
            
        Returns:
            Dict containing the fetched data and metadata
        """
        pass
    
    @abstractmethod
    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a write action on the external platform.
        
        Args:
            action: The action identifier (e.g., 'create_post', 'update_lead')
            payload: The data required for the action
            
        Returns:
            Dict containing the result of the action
        """
        pass

    async def test_connection(self) -> Dict[str, Any]:
        """
        Standardized connection test method.
        """
        try:
            is_valid = await self.validate_credentials()
            if is_valid:
                return {"success": True, "message": "Connection successful"}
            return {"success": False, "message": "Invalid credentials"}
        except Exception as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return {"success": False, "message": f"Connection failed: {str(e)}"}

    def track_event(
        self, 
        event_code: str, 
        quantity: float = 1.0, 
        resource_type: str = None,
        metadata: dict = None,
        db_session = None
    ) -> None:
        """
        Track a billable usage event for this connector.
        
        Args:
            event_code: Specific event identifier (e.g., 'post_synced', 'ad_optimized')
            quantity: Number of units for this event
            resource_type: Type of resource affected (e.g., 'posts', 'contacts')
            metadata: Additional event context
            db_session: SQLAlchemy session for persistence
        """
        if db_session is None:
            self.logger.debug(f"Billing event skipped (no db): {event_code}")
            return
        
        try:
            from app.models.billing_event import BillingEventService
            service = BillingEventService(db_session)
            service.track_event(
                tenant_id=self.tenant_id,
                event_type="connector_synced" if "sync" in event_code else "connector_action",
                event_code=event_code,
                quantity=quantity,
                connector_id=self.config.id,
                resource_type=resource_type,
                metadata=metadata or {}
            )
            self.logger.debug(f"Tracked billing event: {event_code} x{quantity}")
        except Exception as e:
            self.logger.warning(f"Failed to track billing event: {e}")

