from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class OAuthMixin(ABC):
    """
    Mixin for connectors that require OAuth authentication.
    """
    
    @abstractmethod
    async def get_auth_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate the authorization URL for the provider.
        """
        pass
    
    @abstractmethod
    async def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Exchange the authorization code for access tokens.
        Should return a dictionary containing access_token, refresh_token, etc.
        """
        pass
    
    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh the access token using the refresh token.
        """
        pass
