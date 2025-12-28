from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class EmailList(BaseModel):
    id: Optional[str] = None
    name: str
    subscriber_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Subscriber(BaseModel):
    id: Optional[str] = None
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: str = "subscribed"  # subscribed, unsubscribed, pending, cleaned
    list_ids: List[str] = []
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}
    subscribed_at: Optional[datetime] = None

class Campaign(BaseModel):
    id: Optional[str] = None
    name: str
    subject: Optional[str] = None
    from_name: Optional[str] = None
    from_email: Optional[str] = None
    list_ids: List[str] = []
    status: str = "draft"  # draft, scheduled, sending, sent, paused, cancelled
    content_html: Optional[str] = None
    content_text: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CampaignStats(BaseModel):
    campaign_id: str
    emails_sent: int = 0
    opens: int = 0
    clicks: int = 0
    bounces: int = 0
    unsubscribes: int = 0
    open_rate: float = 0.0
    click_rate: float = 0.0

class MarketingStats(BaseModel):
    lists: int
    subscribers: int
    campaigns: int
    active_campaigns: int
    last_sync: Optional[datetime] = None

class MarketingPort(ABC):
    """
    Abstract Port for Marketing/Email platforms (Mailchimp, SendGrid, etc).
    """

    @abstractmethod
    async def get_stats(self) -> MarketingStats:
        """Get marketing statistics"""
        pass
    
    # List methods
    @abstractmethod
    async def get_lists(self, limit: int = 100) -> List[EmailList]:
        """Get email lists"""
        pass
    
    @abstractmethod
    async def get_list(self, list_id: str) -> Optional[EmailList]:
        """Get a specific list by ID"""
        pass

    @abstractmethod
    async def create_list(self, email_list: EmailList) -> EmailList:
        """Create a new email list"""
        pass
    
    # Subscriber methods
    @abstractmethod
    async def get_subscribers(self, list_id: str, limit: int = 100) -> List[Subscriber]:
        """Get subscribers from a list"""
        pass
    
    @abstractmethod
    async def get_subscriber(self, list_id: str, subscriber_id: str) -> Optional[Subscriber]:
        """Get a specific subscriber"""
        pass

    @abstractmethod
    async def add_subscriber(self, list_id: str, subscriber: Subscriber) -> Subscriber:
        """Add a subscriber to a list"""
        pass
        
    @abstractmethod
    async def update_subscriber(self, list_id: str, subscriber_id: str, updates: Dict[str, Any]) -> Subscriber:
        """Update a subscriber"""
        pass
    
    @abstractmethod
    async def remove_subscriber(self, list_id: str, subscriber_id: str) -> bool:
        """Remove a subscriber from a list"""
        pass
    
    # Campaign methods
    @abstractmethod
    async def get_campaigns(self, limit: int = 100, status: Optional[str] = None) -> List[Campaign]:
        """Get campaigns"""
        pass
    
    @abstractmethod
    async def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """Get a specific campaign by ID"""
        pass

    @abstractmethod
    async def create_campaign(self, campaign: Campaign) -> Campaign:
        """Create a new campaign"""
        pass
        
    @abstractmethod
    async def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Campaign:
        """Update a campaign"""
        pass
    
    @abstractmethod
    async def send_campaign(self, campaign_id: str) -> bool:
        """Send a campaign"""
        pass
    
    @abstractmethod
    async def get_campaign_stats(self, campaign_id: str) -> CampaignStats:
        """Get campaign statistics"""
        pass
