"""
Platform API clients for real campaign execution
Integrates with Google Ads, Meta Ads, and LinkedIn using BYOK credentials
"""

from .google_ads_client import GoogleAdsClient
from .meta_ads_client import MetaAdsClient  
from .linkedin_ads_client import LinkedInAdsClient

__all__ = [
    'GoogleAdsClient',
    'MetaAdsClient', 
    'LinkedInAdsClient'
]