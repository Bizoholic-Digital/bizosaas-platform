import httpx
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseConnector, ConnectorConfig, ConnectorType, ConnectorStatus
from .registry import ConnectorRegistry
from ..ports.marketing_port import MarketingPort, EmailList, Subscriber, Campaign, CampaignStats, MarketingStats

logger = logging.getLogger(__name__)

@ConnectorRegistry.register
class MailchimpConnector(BaseConnector, MarketingPort):
    @classmethod
    def get_config(cls) -> ConnectorConfig:
        return ConnectorConfig(
            id="mailchimp",
            name="Mailchimp",
            type=ConnectorType.MARKETING,
            description="Manage your email subscribers, audiences, and campaign performance.",
            icon="mail",
            version="2.0.0",
            auth_schema={
                "api_key": {"type": "string", "label": "API Key", "format": "password"},
                "server_prefix": {"type": "string", "label": "Server Prefix", "placeholder": "e.g., us20"}
            }
        )

    def _get_base_url(self) -> str:
        server = self.credentials.get("server_prefix", "us1")
        return f"https://{server}.api.mailchimp.com/3.0"
    
    def _get_auth(self) -> tuple:
        api_key = self.credentials.get("api_key")
        return ("user", api_key)

    async def validate_credentials(self) -> bool:
        api_key = self.credentials.get("api_key")
        if not api_key:
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/", 
                    auth=self._get_auth()
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Mailchimp credential validation failed: {e}")
            return False

    async def get_status(self) -> ConnectorStatus:
        if await self.validate_credentials():
            return ConnectorStatus.CONNECTED
        return ConnectorStatus.ERROR

    # Marketing Port Implementation
    async def get_stats(self) -> MarketingStats:
        """Get marketing statistics from Mailchimp"""
        try:
            async with httpx.AsyncClient() as client:
                # Get lists count
                lists_resp = await client.get(
                    f"{self._get_base_url()}/lists",
                    auth=self._get_auth(),
                    params={"count": 1}
                )
                lists_data = lists_resp.json() if lists_resp.status_code == 200 else {}
                
                # Get campaigns count
                campaigns_resp = await client.get(
                    f"{self._get_base_url()}/campaigns",
                    auth=self._get_auth(),
                    params={"count": 1}
                )
                campaigns_data = campaigns_resp.json() if campaigns_resp.status_code == 200 else {}
                
                return MarketingStats(
                    lists=lists_data.get("total_items", 0),
                    subscribers=0,  # Would need to sum across lists
                    campaigns=campaigns_data.get("total_items", 0),
                    active_campaigns=0
                )
        except Exception as e:
            logger.error(f"Failed to get Mailchimp stats: {e}")
            return MarketingStats(lists=0, subscribers=0, campaigns=0, active_campaigns=0)

    async def get_lists(self, limit: int = 100) -> List[EmailList]:
        """Get email lists from Mailchimp"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/lists",
                    auth=self._get_auth(),
                    params={"count": min(limit, 1000)}
                )
                response.raise_for_status()
                data = response.json()
                
                lists = []
                for item in data.get("lists", []):
                    lists.append(EmailList(
                        id=item.get("id"),
                        name=item.get("name"),
                        subscriber_count=item.get("stats", {}).get("member_count", 0),
                        created_at=datetime.fromisoformat(item.get("date_created").replace("Z", "+00:00")) if item.get("date_created") else None
                    ))
                
                return lists
        except Exception as e:
            logger.error(f"Failed to get Mailchimp lists: {e}")
            return []

    async def get_list(self, list_id: str) -> Optional[EmailList]:
        """Get a specific list by ID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/lists/{list_id}",
                    auth=self._get_auth()
                )
                if response.status_code == 404:
                    return None
                    
                response.raise_for_status()
                item = response.json()
                
                return EmailList(
                    id=item.get("id"),
                    name=item.get("name"),
                    subscriber_count=item.get("stats", {}).get("member_count", 0),
                    created_at=datetime.fromisoformat(item.get("date_created").replace("Z", "+00:00")) if item.get("date_created") else None
                )
        except Exception as e:
            logger.error(f"Failed to get Mailchimp list {list_id}: {e}")
            return None

    async def create_list(self, email_list: EmailList) -> EmailList:
        """Create a new email list"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/lists",
                    auth=self._get_auth(),
                    json={
                        "name": email_list.name,
                        "permission_reminder": "You signed up for updates",
                        "email_type_option": True,
                        "contact": {
                            "company": "BizOSaaS",
                            "address1": "",
                            "city": "",
                            "state": "",
                            "zip": "",
                            "country": "US"
                        },
                        "campaign_defaults": {
                            "from_name": "BizOSaaS",
                            "from_email": "noreply@bizosaas.com",
                            "subject": "",
                            "language": "en"
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                email_list.id = result.get("id")
                return email_list
        except Exception as e:
            logger.error(f"Failed to create Mailchimp list: {e}")
            raise

    async def delete_list(self, list_id: str) -> bool:
        """Delete an email list"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self._get_base_url()}/lists/{list_id}",
                    auth=self._get_auth()
                )
                return response.status_code == 204
        except Exception as e:
            logger.error(f"Failed to delete Mailchimp list {list_id}: {e}")
            return False

    async def get_subscribers(self, list_id: str, limit: int = 100) -> List[Subscriber]:
        """Get subscribers from a list"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/lists/{list_id}/members",
                    auth=self._get_auth(),
                    params={"count": min(limit, 1000)}
                )
                response.raise_for_status()
                data = response.json()
                
                subscribers = []
                for item in data.get("members", []):
                    merge_fields = item.get("merge_fields", {})
                    subscribers.append(Subscriber(
                        id=item.get("id"),
                        email=item.get("email_address"),
                        first_name=merge_fields.get("FNAME"),
                        last_name=merge_fields.get("LNAME"),
                        status=item.get("status"),
                        list_ids=[list_id],
                        custom_fields=merge_fields
                    ))
                
                return subscribers
        except Exception as e:
            logger.error(f"Failed to get Mailchimp subscribers: {e}")
            return []

    async def get_subscriber(self, list_id: str, subscriber_id: str) -> Optional[Subscriber]:
        """Get a specific subscriber"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/lists/{list_id}/members/{subscriber_id}",
                    auth=self._get_auth()
                )
                if response.status_code == 404:
                    return None
                    
                response.raise_for_status()
                item = response.json()
                merge_fields = item.get("merge_fields", {})
                
                return Subscriber(
                    id=item.get("id"),
                    email=item.get("email_address"),
                    first_name=merge_fields.get("FNAME"),
                    last_name=merge_fields.get("LNAME"),
                    status=item.get("status"),
                    list_ids=[list_id],
                    custom_fields=merge_fields
                )
        except Exception as e:
            logger.error(f"Failed to get Mailchimp subscriber: {e}")
            return None

    async def add_subscriber(self, list_id: str, subscriber: Subscriber) -> Subscriber:
        """Add a subscriber to a list"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/lists/{list_id}/members",
                    auth=self._get_auth(),
                    json={
                        "email_address": subscriber.email,
                        "status": subscriber.status,
                        "merge_fields": {
                            "FNAME": subscriber.first_name,
                            "LNAME": subscriber.last_name
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                subscriber.id = result.get("id")
                return subscriber
        except Exception as e:
            logger.error(f"Failed to add Mailchimp subscriber: {e}")
            raise

    async def update_subscriber(self, list_id: str, subscriber_id: str, updates: Dict[str, Any]) -> Subscriber:
        """Update a subscriber"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self._get_base_url()}/lists/{list_id}/members/{subscriber_id}",
                    auth=self._get_auth(),
                    json=updates
                )
                response.raise_for_status()
                return await self.get_subscriber(list_id, subscriber_id)
        except Exception as e:
            logger.error(f"Failed to update Mailchimp subscriber: {e}")
            raise

    async def remove_subscriber(self, list_id: str, subscriber_id: str) -> bool:
        """Remove a subscriber from a list"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self._get_base_url()}/lists/{list_id}/members/{subscriber_id}",
                    auth=self._get_auth()
                )
                return response.status_code == 204
        except Exception as e:
            logger.error(f"Failed to remove Mailchimp subscriber: {e}")
            return False

    async def get_campaigns(self, limit: int = 100, status: Optional[str] = None) -> List[Campaign]:
        """Get campaigns from Mailchimp"""
        try:
            async with httpx.AsyncClient() as client:
                params = {"count": min(limit, 1000)}
                if status:
                    params["status"] = status
                    
                response = await client.get(
                    f"{self._get_base_url()}/campaigns",
                    auth=self._get_auth(),
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                campaigns = []
                for item in data.get("campaigns", []):
                    settings = item.get("settings", {})
                    campaigns.append(Campaign(
                        id=item.get("id"),
                        name=settings.get("title", "Untitled"),
                        subject=settings.get("subject_line"),
                        from_name=settings.get("from_name"),
                        from_email=settings.get("reply_to"),
                        status=item.get("status"),
                        created_at=datetime.fromisoformat(item.get("create_time").replace("Z", "+00:00")) if item.get("create_time") else None
                    ))
                
                return campaigns
        except Exception as e:
            logger.error(f"Failed to get Mailchimp campaigns: {e}")
            return []

    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get a specific campaign by ID"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/campaigns/{campaign_id}",
                    auth=self._get_auth()
                )
                if response.status_code == 404:
                    return None
                    
                response.raise_for_status()
                item = response.json()
                settings = item.get("settings", {})
                
                return Campaign(
                    id=item.get("id"),
                    name=settings.get("title", "Untitled"),
                    subject=settings.get("subject_line"),
                    from_name=settings.get("from_name"),
                    from_email=settings.get("reply_to"),
                    status=item.get("status")
                )
        except Exception as e:
            logger.error(f"Failed to get Mailchimp campaign: {e}")
            return None

    async def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create a new campaign"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/campaigns",
                    auth=self._get_auth(),
                    json={
                        "type": "regular",
                        "settings": {
                            "subject_line": campaign.subject,
                            "title": campaign.name,
                            "from_name": campaign.from_name,
                            "reply_to": campaign.from_email
                        }
                    }
                )
                response.raise_for_status()
                result = response.json()
                campaign.id = result.get("id")
                return campaign
        except Exception as e:
            logger.error(f"Failed to create Mailchimp campaign: {e}")
            raise

    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Campaign:
        """Update a campaign"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self._get_base_url()}/campaigns/{campaign_id}",
                    auth=self._get_auth(),
                    json=updates
                )
                response.raise_for_status()
                return await self.get_campaign(campaign_id)
        except Exception as e:
            logger.error(f"Failed to update Mailchimp campaign: {e}")
            raise

    async def send_campaign(self, campaign_id: str) -> bool:
        """Send a campaign"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._get_base_url()}/campaigns/{campaign_id}/actions/send",
                    auth=self._get_auth()
                )
                return response.status_code == 204
        except Exception as e:
            logger.error(f"Failed to send Mailchimp campaign: {e}")
            return False

    async def delete_campaign(self, campaign_id: str) -> bool:
        """Delete a campaign"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{self._get_base_url()}/campaigns/{campaign_id}",
                    auth=self._get_auth()
                )
                return response.status_code == 204
        except Exception as e:
            logger.error(f"Failed to delete Mailchimp campaign {campaign_id}: {e}")
            return False

    async def get_campaign_stats(self, campaign_id: str) -> CampaignStats:
        """Get campaign statistics"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self._get_base_url()}/reports/{campaign_id}",
                    auth=self._get_auth()
                )
                response.raise_for_status()
                data = response.json()
                
                return CampaignStats(
                    campaign_id=campaign_id,
                    emails_sent=data.get("emails_sent", 0),
                    opens=data.get("opens", {}).get("opens_total", 0),
                    clicks=data.get("clicks", {}).get("clicks_total", 0),
                    bounces=data.get("bounces", {}).get("hard_bounces", 0),
                    unsubscribes=data.get("unsubscribed", 0),
                    open_rate=data.get("opens", {}).get("open_rate", 0.0),
                    click_rate=data.get("clicks", {}).get("click_rate", 0.0)
                )
        except Exception as e:
            logger.error(f"Failed to get Mailchimp campaign stats: {e}")
            return CampaignStats(campaign_id=campaign_id)

    # Legacy methods for backward compatibility
    async def sync_data(self, resource_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Legacy sync support"""
        if resource_type == "lists":
            lists = await self.get_lists()
            return {"data": [l.dict() for l in lists]}
        elif resource_type == "campaigns":
            campaigns = await self.get_campaigns()
            return {"data": [c.dict() for c in campaigns]}
        elif resource_type == "members" and params and params.get("list_id"):
            subscribers = await self.get_subscribers(params["list_id"])
            return {"data": [s.dict() for s in subscribers]}
        return {"error": "Unsupported resource type"}

    async def perform_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy action support"""
        if action == "add_member" and payload.get("list_id") and payload.get("email"):
            subscriber = Subscriber(
                email=payload["email"],
                first_name=payload.get("first_name"),
                last_name=payload.get("last_name"),
                status=payload.get("status", "subscribed")
            )
            result = await self.add_subscriber(payload["list_id"], subscriber)
            return result.dict()
        return {"error": f"Unsupported action: {action}"}
