"""
Integration Registry
Manages the registry of all third-party integrations and their configurations
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

from config.settings import settings, get_integration_config

logger = logging.getLogger(__name__)


class IntegrationCategory(Enum):
    """Integration categories"""
    PAYMENT = "payment"
    MARKETING = "marketing"
    COMMUNICATION = "communication"
    ECOMMERCE = "ecommerce"
    ANALYTICS = "analytics"
    INFRASTRUCTURE = "infrastructure"
    AI = "ai"


class IntegrationStatus(Enum):
    """Integration status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"
    MAINTENANCE = "maintenance"


@dataclass
class IntegrationEndpoint:
    """Integration endpoint configuration"""
    name: str
    url: str
    method: str
    headers: Dict[str, str]
    timeout: int
    expected_status: List[int]
    authentication: Dict[str, Any]
    retry_config: Dict[str, Any]


@dataclass
class Integration:
    """Integration definition"""
    name: str
    display_name: str
    category: IntegrationCategory
    status: IntegrationStatus
    description: str
    vendor: str
    version: str
    endpoints: List[IntegrationEndpoint]
    health_check_endpoint: IntegrationEndpoint
    documentation_url: str
    support_contact: str
    rate_limits: Dict[str, int]
    cost_per_request: float
    priority: str
    tags: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class IntegrationRegistry:
    """
    Central registry for all third-party integrations
    Manages integration configurations, endpoints, and metadata
    """
    
    def __init__(self):
        self.integrations: Dict[str, Integration] = {}
        self.categories: Dict[IntegrationCategory, List[str]] = {}
        
        logger.info("Integration Registry initialized")
    
    async def load_integrations(self):
        """Load all integration configurations"""
        try:
            # Load payment integrations
            await self._load_payment_integrations()
            
            # Load marketing integrations
            await self._load_marketing_integrations()
            
            # Load communication integrations
            await self._load_communication_integrations()
            
            # Load e-commerce integrations
            await self._load_ecommerce_integrations()
            
            # Load analytics integrations
            await self._load_analytics_integrations()
            
            # Load infrastructure integrations
            await self._load_infrastructure_integrations()
            
            # Load AI integrations
            await self._load_ai_integrations()
            
            # Build category index
            self._build_category_index()
            
            logger.info(f"Loaded {len(self.integrations)} integrations across {len(self.categories)} categories")
            
        except Exception as e:
            logger.error(f"Failed to load integrations: {e}")
            raise
    
    async def _load_payment_integrations(self):
        """Load payment gateway integrations"""
        
        # Stripe Integration
        stripe_integration = Integration(
            name="stripe",
            display_name="Stripe",
            category=IntegrationCategory.PAYMENT,
            status=IntegrationStatus.ACTIVE,
            description="Online payment processing platform",
            vendor="Stripe Inc.",
            version="2023-10-16",
            endpoints=[
                IntegrationEndpoint(
                    name="create_payment_intent",
                    url="https://api.stripe.com/v1/payment_intents",
                    method="POST",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30,
                    expected_status=[200, 201],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                ),
                IntegrationEndpoint(
                    name="get_customer",
                    url="https://api.stripe.com/v1/customers/{customer_id}",
                    method="GET",
                    headers={},
                    timeout=15,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 1}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.stripe.com/v1/account",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://stripe.com/docs/api",
            support_contact="support@stripe.com",
            rate_limits={"requests_per_second": 100, "requests_per_hour": 100000},
            cost_per_request=0.001,
            priority="critical",
            tags=["payment", "credit-card", "subscription"],
            metadata={"region": "global", "compliance": ["PCI-DSS", "SOC2"]},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["stripe"] = stripe_integration
        
        # PayPal Integration
        paypal_integration = Integration(
            name="paypal",
            display_name="PayPal",
            category=IntegrationCategory.PAYMENT,
            status=IntegrationStatus.ACTIVE,
            description="Digital payment platform",
            vendor="PayPal Holdings Inc.",
            version="v2",
            endpoints=[
                IntegrationEndpoint(
                    name="create_order",
                    url="https://api.paypal.com/v2/checkout/orders",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[201],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.paypal.com/v1/oauth2/token",
                method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10,
                expected_status=[200],
                authentication={"type": "basic", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developer.paypal.com/docs/api/overview/",
            support_contact="developer-support@paypal.com",
            rate_limits={"requests_per_second": 50, "requests_per_hour": 50000},
            cost_per_request=0.002,
            priority="critical",
            tags=["payment", "digital-wallet"],
            metadata={"region": "global", "compliance": ["PCI-DSS"]},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["paypal"] = paypal_integration
        
        # Razorpay Integration (India)
        razorpay_integration = Integration(
            name="razorpay",
            display_name="Razorpay",
            category=IntegrationCategory.PAYMENT,
            status=IntegrationStatus.ACTIVE,
            description="Indian payment gateway",
            vendor="Razorpay Software Pvt Ltd",
            version="v1",
            endpoints=[
                IntegrationEndpoint(
                    name="create_order",
                    url="https://api.razorpay.com/v1/orders",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "basic", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.razorpay.com/v1/payments",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "basic", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://razorpay.com/docs/api/",
            support_contact="support@razorpay.com",
            rate_limits={"requests_per_second": 30, "requests_per_hour": 10000},
            cost_per_request=0.0015,
            priority="high",
            tags=["payment", "india", "upi"],
            metadata={"region": "india", "compliance": ["RBI"]},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["razorpay"] = razorpay_integration
    
    async def _load_marketing_integrations(self):
        """Load marketing platform integrations"""
        
        # Google Ads Integration
        google_ads_integration = Integration(
            name="google_ads",
            display_name="Google Ads",
            category=IntegrationCategory.MARKETING,
            status=IntegrationStatus.ACTIVE,
            description="Google advertising platform",
            vendor="Google LLC",
            version="v14",
            endpoints=[
                IntegrationEndpoint(
                    name="create_campaign",
                    url="https://googleads.googleapis.com/v14/customers/{customer_id}/campaigns:mutate",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=60,
                    expected_status=[200],
                    authentication={"type": "oauth2", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                ),
                IntegrationEndpoint(
                    name="get_campaigns",
                    url="https://googleads.googleapis.com/v14/customers/{customer_id}/googleAds:search",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "oauth2", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 1}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://googleads.googleapis.com/v14/customers/{customer_id}/campaigns",
                method="GET",
                headers={},
                timeout=15,
                expected_status=[200],
                authentication={"type": "oauth2", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developers.google.com/google-ads/api/docs",
            support_contact="google-ads-api-support@google.com",
            rate_limits={"requests_per_second": 10, "requests_per_day": 50000},
            cost_per_request=0.0,
            priority="high",
            tags=["advertising", "search", "display"],
            metadata={"region": "global", "quota_units": "operations"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["google_ads"] = google_ads_integration
        
        # Facebook Ads Integration
        facebook_ads_integration = Integration(
            name="facebook_ads",
            display_name="Facebook Ads",
            category=IntegrationCategory.MARKETING,
            status=IntegrationStatus.ACTIVE,
            description="Facebook advertising platform",
            vendor="Meta Platforms Inc.",
            version="v18.0",
            endpoints=[
                IntegrationEndpoint(
                    name="create_campaign",
                    url="https://graph.facebook.com/v18.0/act_{account_id}/campaigns",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=60,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                ),
                IntegrationEndpoint(
                    name="get_insights",
                    url="https://graph.facebook.com/v18.0/{campaign_id}/insights",
                    method="GET",
                    headers={},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 1}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://graph.facebook.com/v18.0/me",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developers.facebook.com/docs/marketing-api",
            support_contact="developers@facebook.com",
            rate_limits={"requests_per_hour": 200, "calls_per_day": 4800},
            cost_per_request=0.0,
            priority="high",
            tags=["advertising", "social", "video"],
            metadata={"region": "global", "rate_limit_type": "sliding_window"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["facebook_ads"] = facebook_ads_integration
        
        # LinkedIn Marketing Integration
        linkedin_marketing_integration = Integration(
            name="linkedin_marketing",
            display_name="LinkedIn Marketing",
            category=IntegrationCategory.MARKETING,
            status=IntegrationStatus.ACTIVE,
            description="LinkedIn advertising platform",
            vendor="LinkedIn Corporation",
            version="v2",
            endpoints=[
                IntegrationEndpoint(
                    name="create_campaign",
                    url="https://api.linkedin.com/v2/adCampaignsV2",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=60,
                    expected_status=[201],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.linkedin.com/v2/people/(id~)",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://docs.microsoft.com/en-us/linkedin/marketing/",
            support_contact="marketing-api@linkedin.com",
            rate_limits={"requests_per_day": 500000, "requests_per_hour": 100000},
            cost_per_request=0.0,
            priority="medium",
            tags=["advertising", "b2b", "professional"],
            metadata={"region": "global", "throttle_type": "developer_application"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["linkedin_marketing"] = linkedin_marketing_integration
    
    async def _load_communication_integrations(self):
        """Load communication service integrations"""
        
        # Resend SMTP Integration
        resend_smtp_integration = Integration(
            name="resend_smtp",
            display_name="Resend",
            category=IntegrationCategory.COMMUNICATION,
            status=IntegrationStatus.ACTIVE,
            description="Modern email API for developers",
            vendor="Resend Inc.",
            version="v1",
            endpoints=[
                IntegrationEndpoint(
                    name="send_email",
                    url="https://api.resend.com/emails",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.resend.com/domains",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://resend.com/docs",
            support_contact="support@resend.com",
            rate_limits={"emails_per_day": 100, "emails_per_hour": 10},
            cost_per_request=0.001,
            priority="high",
            tags=["email", "transactional", "smtp"],
            metadata={"region": "global", "deliverability": "high"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["resend_smtp"] = resend_smtp_integration
        
        # Twilio SMS Integration
        twilio_sms_integration = Integration(
            name="twilio_sms",
            display_name="Twilio SMS",
            category=IntegrationCategory.COMMUNICATION,
            status=IntegrationStatus.ACTIVE,
            description="Cloud communications platform",
            vendor="Twilio Inc.",
            version="2010-04-01",
            endpoints=[
                IntegrationEndpoint(
                    name="send_sms",
                    url="https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
                    method="POST",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=30,
                    expected_status=[201],
                    authentication={"type": "basic", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.twilio.com/2010-04-01/Accounts/{account_sid}.json",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "basic", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://www.twilio.com/docs/sms",
            support_contact="support@twilio.com",
            rate_limits={"messages_per_second": 1, "messages_per_hour": 100},
            cost_per_request=0.0075,
            priority="medium",
            tags=["sms", "voice", "messaging"],
            metadata={"region": "global", "delivery_tracking": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["twilio_sms"] = twilio_sms_integration
        
        # WhatsApp Business API Integration
        whatsapp_business_integration = Integration(
            name="whatsapp_business",
            display_name="WhatsApp Business",
            category=IntegrationCategory.COMMUNICATION,
            status=IntegrationStatus.ACTIVE,
            description="WhatsApp Business messaging platform",
            vendor="Meta Platforms Inc.",
            version="v17.0",
            endpoints=[
                IntegrationEndpoint(
                    name="send_message",
                    url="https://graph.facebook.com/v17.0/{phone_number_id}/messages",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://graph.facebook.com/v17.0/{phone_number_id}",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developers.facebook.com/docs/whatsapp",
            support_contact="whatsapp-business@facebook.com",
            rate_limits={"messages_per_second": 20, "messages_per_day": 1000},
            cost_per_request=0.005,
            priority="medium",
            tags=["messaging", "chat", "business"],
            metadata={"region": "global", "template_required": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["whatsapp_business"] = whatsapp_business_integration
    
    async def _load_ecommerce_integrations(self):
        """Load e-commerce platform integrations"""
        
        # Saleor GraphQL Integration
        saleor_graphql_integration = Integration(
            name="saleor_graphql",
            display_name="Saleor",
            category=IntegrationCategory.ECOMMERCE,
            status=IntegrationStatus.ACTIVE,
            description="Headless e-commerce platform",
            vendor="Saleor Commerce",
            version="3.15",
            endpoints=[
                IntegrationEndpoint(
                    name="graphql_query",
                    url="https://demo.saleor.io/graphql/",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://demo.saleor.io/graphql/",
                method="POST",
                headers={"Content-Type": "application/json"},
                timeout=10,
                expected_status=[200],
                authentication={"type": "none"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://docs.saleor.io/",
            support_contact="support@saleor.io",
            rate_limits={"requests_per_second": 100, "requests_per_minute": 1000},
            cost_per_request=0.0,
            priority="medium",
            tags=["ecommerce", "graphql", "headless"],
            metadata={"region": "global", "self_hosted": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["saleor_graphql"] = saleor_graphql_integration
        
        # Amazon SP-API Integration
        amazon_sp_api_integration = Integration(
            name="amazon_sp_api",
            display_name="Amazon SP-API",
            category=IntegrationCategory.ECOMMERCE,
            status=IntegrationStatus.ACTIVE,
            description="Amazon Selling Partner API",
            vendor="Amazon.com Inc.",
            version="2021-06-30",
            endpoints=[
                IntegrationEndpoint(
                    name="get_orders",
                    url="https://sellingpartnerapi-na.amazon.com/orders/v0/orders",
                    method="GET",
                    headers={},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "aws_sig4", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://sellingpartnerapi-na.amazon.com/orders/v0/orders",
                method="GET",
                headers={},
                timeout=15,
                expected_status=[200, 403],  # 403 is acceptable for auth check
                authentication={"type": "aws_sig4", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developer-docs.amazon.com/sp-api/",
            support_contact="selling-partner-api-developer-support@amazon.com",
            rate_limits={"requests_per_second": 0.5, "requests_per_hour": 3600},
            cost_per_request=0.0,
            priority="high",
            tags=["marketplace", "fulfillment", "inventory"],
            metadata={"region": "multiple", "requires_approval": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["amazon_sp_api"] = amazon_sp_api_integration
    
    async def _load_analytics_integrations(self):
        """Load analytics platform integrations"""
        
        # Google Analytics Integration
        google_analytics_integration = Integration(
            name="google_analytics",
            display_name="Google Analytics",
            category=IntegrationCategory.ANALYTICS,
            status=IntegrationStatus.ACTIVE,
            description="Web analytics platform",
            vendor="Google LLC",
            version="GA4",
            endpoints=[
                IntegrationEndpoint(
                    name="run_report",
                    url="https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=60,
                    expected_status=[200],
                    authentication={"type": "oauth2", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://analyticsdata.googleapis.com/v1beta/properties/{property_id}/metadata",
                method="GET",
                headers={},
                timeout=15,
                expected_status=[200],
                authentication={"type": "oauth2", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developers.google.com/analytics/devguides/reporting/data/v1",
            support_contact="analytics-api-support@google.com",
            rate_limits={"requests_per_day": 50000, "requests_per_100_seconds": 1500},
            cost_per_request=0.0,
            priority="medium",
            tags=["analytics", "web", "tracking"],
            metadata={"region": "global", "sampling": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["google_analytics"] = google_analytics_integration
        
        # Facebook Pixel Integration
        facebook_pixel_integration = Integration(
            name="facebook_pixel",
            display_name="Facebook Pixel",
            category=IntegrationCategory.ANALYTICS,
            status=IntegrationStatus.ACTIVE,
            description="Facebook tracking pixel for ads optimization",
            vendor="Meta Platforms Inc.",
            version="v18.0",
            endpoints=[
                IntegrationEndpoint(
                    name="send_events",
                    url="https://graph.facebook.com/v18.0/{pixel_id}/events",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://graph.facebook.com/v18.0/{pixel_id}",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developers.facebook.com/docs/marketing-api/conversions-api",
            support_contact="developers@facebook.com",
            rate_limits={"events_per_hour": 1000000, "events_per_second": 1000},
            cost_per_request=0.0,
            priority="medium",
            tags=["tracking", "conversion", "advertising"],
            metadata={"region": "global", "real_time": True},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["facebook_pixel"] = facebook_pixel_integration
    
    async def _load_infrastructure_integrations(self):
        """Load infrastructure service integrations"""
        
        # AWS S3 Integration
        aws_s3_integration = Integration(
            name="aws_s3",
            display_name="Amazon S3",
            category=IntegrationCategory.INFRASTRUCTURE,
            status=IntegrationStatus.ACTIVE,
            description="Object storage service",
            vendor="Amazon Web Services",
            version="2006-03-01",
            endpoints=[
                IntegrationEndpoint(
                    name="put_object",
                    url="https://{bucket}.s3.amazonaws.com/{key}",
                    method="PUT",
                    headers={},
                    timeout=300,
                    expected_status=[200],
                    authentication={"type": "aws_sig4", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                ),
                IntegrationEndpoint(
                    name="get_object",
                    url="https://{bucket}.s3.amazonaws.com/{key}",
                    method="GET",
                    headers={},
                    timeout=60,
                    expected_status=[200],
                    authentication={"type": "aws_sig4", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 1}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://{bucket}.s3.amazonaws.com/",
                method="HEAD",
                headers={},
                timeout=10,
                expected_status=[200, 403],  # 403 is acceptable for bucket existence check
                authentication={"type": "aws_sig4", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://docs.aws.amazon.com/s3/",
            support_contact="aws-support@amazon.com",
            rate_limits={"requests_per_second": 3500, "put_requests_per_second": 3500},
            cost_per_request=0.0004,
            priority="critical",
            tags=["storage", "cdn", "backup"],
            metadata={"region": "multiple", "durability": "99.999999999%"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["aws_s3"] = aws_s3_integration
        
        # CloudFlare Integration
        cloudflare_integration = Integration(
            name="cloudflare",
            display_name="CloudFlare",
            category=IntegrationCategory.INFRASTRUCTURE,
            status=IntegrationStatus.ACTIVE,
            description="Web performance and security service",
            vendor="Cloudflare Inc.",
            version="v4",
            endpoints=[
                IntegrationEndpoint(
                    name="purge_cache",
                    url="https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=30,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.cloudflare.com/client/v4/user",
                method="GET",
                headers={},
                timeout=10,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://developers.cloudflare.com/api/",
            support_contact="support@cloudflare.com",
            rate_limits={"requests_per_minute": 1200, "requests_per_hour": 100000},
            cost_per_request=0.0,
            priority="critical",
            tags=["cdn", "security", "dns"],
            metadata={"region": "global", "edge_locations": 250},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["cloudflare"] = cloudflare_integration
    
    async def _load_ai_integrations(self):
        """Load AI service integrations"""
        
        # OpenAI Integration
        openai_integration = Integration(
            name="openai",
            display_name="OpenAI",
            category=IntegrationCategory.AI,
            status=IntegrationStatus.ACTIVE,
            description="AI language models and API",
            vendor="OpenAI Inc.",
            version="v1",
            endpoints=[
                IntegrationEndpoint(
                    name="chat_completions",
                    url="https://api.openai.com/v1/chat/completions",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=120,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                ),
                IntegrationEndpoint(
                    name="embeddings",
                    url="https://api.openai.com/v1/embeddings",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=60,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 1}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.openai.com/v1/models",
                method="GET",
                headers={},
                timeout=15,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://platform.openai.com/docs/api-reference",
            support_contact="support@openai.com",
            rate_limits={"requests_per_minute": 3500, "tokens_per_minute": 90000},
            cost_per_request=0.002,
            priority="medium",
            tags=["ai", "llm", "chat", "embeddings"],
            metadata={"region": "global", "models": ["gpt-4", "gpt-3.5-turbo"]},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["openai"] = openai_integration
        
        # Anthropic Claude Integration
        anthropic_integration = Integration(
            name="anthropic",
            display_name="Anthropic Claude",
            category=IntegrationCategory.AI,
            status=IntegrationStatus.ACTIVE,
            description="Claude AI assistant",
            vendor="Anthropic Inc.",
            version="v1",
            endpoints=[
                IntegrationEndpoint(
                    name="messages",
                    url="https://api.anthropic.com/v1/messages",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=120,
                    expected_status=[200],
                    authentication={"type": "x-api-key", "header": "x-api-key"},
                    retry_config={"max_retries": 3, "backoff_factor": 2}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.anthropic.com/v1/messages",
                method="POST",
                headers={"Content-Type": "application/json"},
                timeout=15,
                expected_status=[200, 400],  # 400 is acceptable for malformed request
                authentication={"type": "x-api-key", "header": "x-api-key"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://docs.anthropic.com/claude/reference",
            support_contact="support@anthropic.com",
            rate_limits={"requests_per_minute": 1000, "tokens_per_minute": 40000},
            cost_per_request=0.003,
            priority="medium",
            tags=["ai", "llm", "assistant"],
            metadata={"region": "global", "models": ["claude-3", "claude-2"]},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["anthropic"] = anthropic_integration
        
        # Synthesia.io Integration
        synthesia_integration = Integration(
            name="synthesia",
            display_name="Synthesia",
            category=IntegrationCategory.AI,
            status=IntegrationStatus.ACTIVE,
            description="AI video generation platform",
            vendor="Synthesia Ltd.",
            version="v1",
            endpoints=[
                IntegrationEndpoint(
                    name="create_video",
                    url="https://api.synthesia.io/v1/videos",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=300,
                    expected_status=[201],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 3}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.synthesia.io/v1/avatars",
                method="GET",
                headers={},
                timeout=15,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://docs.synthesia.io/",
            support_contact="support@synthesia.io",
            rate_limits={"videos_per_month": 100, "concurrent_renders": 3},
            cost_per_request=2.50,
            priority="low",
            tags=["ai", "video", "avatar"],
            metadata={"region": "global", "processing_time": "5-10 minutes"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["synthesia"] = synthesia_integration
        
        # Midjourney Integration (placeholder - actual API may differ)
        midjourney_integration = Integration(
            name="midjourney",
            display_name="Midjourney",
            category=IntegrationCategory.AI,
            status=IntegrationStatus.MAINTENANCE,
            description="AI image generation platform",
            vendor="Midjourney Inc.",
            version="v1",
            endpoints=[
                IntegrationEndpoint(
                    name="generate_image",
                    url="https://api.midjourney.com/v1/imagine",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    timeout=180,
                    expected_status=[200],
                    authentication={"type": "bearer", "header": "Authorization"},
                    retry_config={"max_retries": 2, "backoff_factor": 3}
                )
            ],
            health_check_endpoint=IntegrationEndpoint(
                name="health_check",
                url="https://api.midjourney.com/v1/status",
                method="GET",
                headers={},
                timeout=15,
                expected_status=[200],
                authentication={"type": "bearer", "header": "Authorization"},
                retry_config={"max_retries": 1, "backoff_factor": 1}
            ),
            documentation_url="https://docs.midjourney.com/",
            support_contact="support@midjourney.com",
            rate_limits={"images_per_hour": 25, "concurrent_jobs": 3},
            cost_per_request=0.08,
            priority="low",
            tags=["ai", "image", "art"],
            metadata={"region": "global", "processing_time": "1-2 minutes"},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.integrations["midjourney"] = midjourney_integration
    
    def _build_category_index(self):
        """Build category-based index of integrations"""
        self.categories = {category: [] for category in IntegrationCategory}
        
        for integration_name, integration in self.integrations.items():
            self.categories[integration.category].append(integration_name)
        
        logger.info(f"Built category index: {dict((k.value, len(v)) for k, v in self.categories.items())}")
    
    # Public API methods
    
    async def get_integration(self, name: str) -> Optional[Integration]:
        """Get integration by name"""
        return self.integrations.get(name)
    
    async def get_all_integrations(self) -> Dict[str, Integration]:
        """Get all integrations"""
        return self.integrations.copy()
    
    async def get_active_integrations(self) -> List[Dict[str, Any]]:
        """Get all active integrations"""
        active_integrations = []
        for name, integration in self.integrations.items():
            if integration.status == IntegrationStatus.ACTIVE:
                active_integrations.append({
                    'name': name,
                    'display_name': integration.display_name,
                    'category': integration.category.value,
                    'vendor': integration.vendor,
                    'priority': integration.priority,
                    'health_check_endpoint': asdict(integration.health_check_endpoint),
                    'rate_limits': integration.rate_limits,
                    'cost_per_request': integration.cost_per_request
                })
        return active_integrations
    
    async def get_integrations_by_category(self, category: str) -> List[str]:
        """Get integrations by category"""
        try:
            category_enum = IntegrationCategory(category)
            return self.categories.get(category_enum, [])
        except ValueError:
            return []
    
    async def get_integration_categories(self) -> Dict[str, List[str]]:
        """Get all categories with their integrations"""
        return {category.value: integration_names for category, integration_names in self.categories.items()}
    
    async def get_integration_summary(self) -> Dict[str, Any]:
        """Get summary of all integrations"""
        total = len(self.integrations)
        active = len([i for i in self.integrations.values() if i.status == IntegrationStatus.ACTIVE])
        by_category = {cat.value: len(integrations) for cat, integrations in self.categories.items()}
        by_priority = {}
        by_vendor = {}
        
        for integration in self.integrations.values():
            # Count by priority
            priority = integration.priority
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            # Count by vendor
            vendor = integration.vendor
            by_vendor[vendor] = by_vendor.get(vendor, 0) + 1
        
        return {
            'total_integrations': total,
            'active_integrations': active,
            'inactive_integrations': total - active,
            'by_category': by_category,
            'by_priority': by_priority,
            'by_vendor': by_vendor,
            'total_endpoints': sum(len(i.endpoints) for i in self.integrations.values()),
            'average_cost_per_request': sum(i.cost_per_request for i in self.integrations.values()) / total if total > 0 else 0
        }
    
    async def update_integration_status(self, name: str, status: str) -> bool:
        """Update integration status"""
        integration = self.integrations.get(name)
        if not integration:
            return False
        
        try:
            integration.status = IntegrationStatus(status)
            integration.updated_at = datetime.now()
            logger.info(f"Updated {name} status to {status}")
            return True
        except ValueError:
            logger.error(f"Invalid status: {status}")
            return False
    
    async def add_custom_integration(self, integration_config: Dict[str, Any]) -> bool:
        """Add custom integration configuration"""
        try:
            # Validate required fields
            required_fields = ['name', 'display_name', 'category', 'health_check_endpoint']
            for field in required_fields:
                if field not in integration_config:
                    logger.error(f"Missing required field: {field}")
                    return False
            
            # Create integration object
            integration = Integration(
                name=integration_config['name'],
                display_name=integration_config['display_name'],
                category=IntegrationCategory(integration_config['category']),
                status=IntegrationStatus(integration_config.get('status', 'active')),
                description=integration_config.get('description', ''),
                vendor=integration_config.get('vendor', 'Custom'),
                version=integration_config.get('version', '1.0'),
                endpoints=[],  # Would be parsed from config
                health_check_endpoint=integration_config['health_check_endpoint'],
                documentation_url=integration_config.get('documentation_url', ''),
                support_contact=integration_config.get('support_contact', ''),
                rate_limits=integration_config.get('rate_limits', {}),
                cost_per_request=integration_config.get('cost_per_request', 0.0),
                priority=integration_config.get('priority', 'medium'),
                tags=integration_config.get('tags', []),
                metadata=integration_config.get('metadata', {}),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Add to registry
            self.integrations[integration.name] = integration
            
            # Update category index
            category = integration.category
            if category not in self.categories:
                self.categories[category] = []
            self.categories[category].append(integration.name)
            
            logger.info(f"Added custom integration: {integration.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add custom integration: {e}")
            return False