from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    id: Optional[str] = None
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    currency: str = "USD"
    payment_provider_id: Optional[str] = None # e.g. Stripe Customer ID
    metadata: Dict[str, Any] = {}

class SubscriptionPlan(BaseModel):
    id: str
    name: str
    code: str
    amount: float
    currency: str
    interval: str # month, year
    trial_period_days: Optional[int] = 0

class Subscription(BaseModel):
    id: Optional[str] = None
    customer_id: str
    plan_id: str
    status: str # active, trialing, past_due, canceled
    current_period_start: datetime
    current_period_end: datetime
    cancel_at_period_end: bool = False

class Invoice(BaseModel):
    id: str
    customer_id: str
    subscription_id: Optional[str] = None
    amount_due: float
    currency: str
    status: str # paid, open, void, uncollectible
    invoice_pdf_url: Optional[str] = None
    created_at: datetime

class BillingPort(ABC):
    """
    Abstract Port for Billing & Subscription platforms (Lago, Stripe).
    """

    @abstractmethod
    async def create_customer(self, customer: Customer) -> Customer:
        pass
        
    @abstractmethod
    async def get_customer(self, customer_id: str) -> Optional[Customer]:
        pass

    @abstractmethod
    async def get_plans(self) -> List[SubscriptionPlan]:
        pass

    @abstractmethod
    async def create_subscription(self, customer_id: str, plan_code: str) -> Subscription:
        pass

    @abstractmethod
    async def cancel_subscription(self, subscription_id: str) -> bool:
        pass

    @abstractmethod
    async def get_customer_subscriptions(self, customer_id: str) -> List[Subscription]:
        pass

    @abstractmethod
    async def get_customer_invoices(self, customer_id: str) -> List[Invoice]:
        pass
