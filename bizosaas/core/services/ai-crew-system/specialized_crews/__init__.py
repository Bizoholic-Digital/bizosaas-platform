"""
Specialized Crews for BizOSaaS Platform

This module contains domain-specific crew implementations for different
business areas including CRM, E-commerce, Analytics, Billing, CMS, and Integrations.
"""

from .crm_crew import CRMSpecializedCrew
from .ecommerce_crew import EcommerceSpecializedCrew
from .analytics_crew import AnalyticsSpecializedCrew
from .billing_crew import BillingSpecializedCrew
from .cms_crew import CMSSpecializedCrew
from .integrations_crew import IntegrationsSpecializedCrew

__all__ = [
    "CRMSpecializedCrew",
    "EcommerceSpecializedCrew", 
    "AnalyticsSpecializedCrew",
    "BillingSpecializedCrew",
    "CMSSpecializedCrew",
    "IntegrationsSpecializedCrew"
]