import httpx
from typing import Dict, Any, Optional
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry

@ConnectorRegistry.register
class GoogleAnalyticsConnector(BaseConnector):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="google-analytics",
            name="Google Analytics 4",
            type=ConnectorType.ANALYTICS,
            description="Track website traffic, user behavior, and conversion metrics.",
            icon="google-analytics",
            version="1.0.0",
            auth_schema={
                "property_id": {"type": "string", "label": "GA4 Property ID"},
                "client_email": {"type": "string", "label": "Service Account Email"},
                "private_key": {"type": "string", "label": "Private Key", "format": "textarea", "help": "From Google Cloud Service Account JSON"}
            }
        )

    async def _get_access_token(self) -> str:
        # NOTE: In a production environment, we would use the google-auth library 
        # to sign the JWT and exchange it for an access token.
        # For this prototype/MVP, we will assume the user might provide a pre-generated 
        # access token in the credentials for simplicity, OR we'd implement the full 
        # JWT flow.
        
        # To keep dependencies minimal and avoid complex crypto in this snippet,
        # we'll assume an 'access_token' is provided in credentials for the MVP test,
        # or mock the behavior if not present but 'mock_mode' is on.
        
        if self.credentials.get("access_token"):
            return self.credentials.get("access_token")
            
        # TODO: Implement full Service Account JWT flow using google-auth or pyjwt
        # For now, raise error if no token
        raise NotImplementedError("Full Service Account auth flow requires 'google-auth' package. Please provide a temporary 'access_token' in credentials for testing.")

    async def validate_credentials(self) -> bool:
        try:
            token = await self._get_access_token()
            # Simple metadata check
            property_id = self.credentials.get("property_id")
            url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}/metadata"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Fetch reports from GA4.
        resource_type: 'basic_report'
        """
        property_id = self.credentials.get("property_id")
        url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
        
        # Default report request
        report_request = {
            "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
            "dimensions": [{"name": "date"}],
            "metrics": [{"name": "activeUsers"}, {"name": "sessions"}]
        }
        
        # Allow overriding via params
        if params and "request_body" in params:
            report_request = params["request_body"]

        try:
            token = await self._get_access_token()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers={"Authorization": f"Bearer {token}"},
                    json=report_request,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            self.logger.error(f"Sync failed for {resource_type}: {e}")
            raise

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Google Analytics connector is read-only")
