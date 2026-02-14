from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseConnectorPort(ABC):
    """
    Base contract for all external system connectors.
    """
    
    @abstractmethod
    async def validate_credentials(self, credentials: Dict[str, Any]) -> bool:
        """Verify that the provided credentials work."""
        pass

    @abstractmethod
    async def get_health(self) -> Dict[str, Any]:
        """Check connection health and latency."""
        pass
    
    @abstractmethod
    async def get_authorize_url(self, state: str) -> str:
        """Return OAuth authorization URL if applicable."""
        pass

    @abstractmethod
    async def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """Exchange OAuth code for access tokens."""
        pass
